from collections import Counter

import berserk
import chess
import gradio as gr
import polars as pl
from chess.pgn import Headers

from chessli2.settings import get_client
from chessli2.writer import write_pgn_to_csv_with_tags

puzzle_db_csv = "lichess_db_puzzles.csv"


def generate_puzzle_history_pgn(puzzle_activity):
    game = puzzle_activity["game"]
    puzzle = puzzle_activity["puzzle"]
    themes = puzzle["themes"]

    board = chess.Board()
    moves = game["pgn"].split()

    for move in moves[:-1]:
        board.push_san(move)
    last_move = board.parse_san(moves[-1])

    pgn = chess.pgn.Game(
        headers={
            "Event": "Puzzle",
            "Site": f"https://www.lichess.org/training/{puzzle['id']}",
            "Themes": " ".join(themes),
        }
    )
    pgn.setup(board)
    puzzle_moves = [chess.Move.from_uci(m) for m in puzzle["solution"]]

    pgn.add_line(
        moves=[last_move] + puzzle_moves,
        starting_comment=f"Puzzle {puzzle['id']} with themes: {' '.join(puzzle['themes'])}",
    )

    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
    pgn_string = pgn.accept(exporter)
    return pgn_string, themes


def get_puzzle_history(before, max, themes_selection, lichess_api_token):
    client, lichess_api_token = get_client(lichess_api_token=lichess_api_token)

    puzzle_activity = client.puzzles.get_puzzle_activity(
        before=berserk.utils.to_millis(before), max=max
    )
    n_puzzles = 0
    skipped_puzzles = 0
    puzzle_pgns = []
    # Create a counter object that tracks the number of puzzles per theme
    theme_counter = Counter()

    try:
        for pa in puzzle_activity:
            ppgn, themes = generate_puzzle_history_pgn(
                client.puzzles.get(pa["puzzle"]["id"])
            )
            # check if any of the selected themes are in the puzzle themes
            if not set(themes_selection).isdisjoint(themes):
                n_puzzles += 1
                theme_counter.update(themes)
                puzzle_pgns.append((ppgn, " ".join(themes)))
            else:
                skipped_puzzles += 1
            download_info = (
                f"Fetched {n_puzzles}, skipped {skipped_puzzles} puzzle(s)..."
            )
            yield puzzle_pgns, theme_counter, gr.DownloadButton(
                label=download_info, variant="secondary", visible=True
            )

        if n_puzzles > 0:
            filename = "puzzles.csv"
            write_pgn_to_csv_with_tags(puzzle_pgns, filename=filename)
            download_info = f"Download CSV file with PGNs of {n_puzzles} puzzles"
            yield puzzle_pgns, theme_counter, gr.DownloadButton(
                value=filename, label=download_info, variant="primary"
            )
        else:
            yield puzzle_pgns, {"Puzzles": 0}, gr.DownloadButton(
                label="No puzzles found", variant="secondary"
            )
    except berserk.exceptions.ResponseError as e:
        if "No such token" in e.message:
            gr.Warning("Your lichess API token is invalid. Did you misspell it?")
            warning = "Please insert a correct lichess API token into the textbox at the top of the interface"
        else:
            gr.Warning(
                "To fetch your puzzle activity, you need to authenticate with your lichess API token!"
            )
            warning = "Please paste your lichess API token into the corresponding textbox at the top of the interface to fetch your puzzles"
        yield "", {}, gr.DownloadButton(
            label=warning,
            visible=True,
            variant="stop",
        )


def generate_puzzle_db_pgn(id, fen, moves, themes):
    board = chess.Board(fen)

    move_list = moves.split()
    for move in move_list:
        board.push(chess.Move.from_uci(move))

    game = chess.pgn.Game.from_board(board)
    game.headers = Headers(
        {
            "Event": "Puzzle",
            "Site": f"https://www.lichess.org/training/{id}",
            "Themes": themes,
            "FEN": fen,
            "SetUp": "1",
        }
    )
    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
    pgn_string = game.accept(exporter)

    return pgn_string


def get_puzzles_from_db(
    themes=None,
    popularity_range=None,
    rating_range=None,
    nb_plays_range=None,
    opening_tags=None,
    max=1000,
    progress=gr.Progress(),
):
    """
    Filters the puzzles based on the provided criteria.

    Parameters:
    - df (pl.DataFrame): The Polars DataFrame containing the puzzle data.
    - themes (list of str): List of themes to filter by.
    - popularity_range (tuple of int): Tuple containing the min and max popularity scores.
    - rating_range (tuple of int): Tuple containing the min and max ratings.
    - nb_plays_range (tuple of int): Tuple containing the min and max number of plays.
    - opening_tags (list of str): List of opening tags to filter by.

    Returns:
    - pl.DataFrame: The filtered DataFrame.
    """
    df = pl.scan_csv(puzzle_db_csv)

    if popularity_range:
        min_popularity, max_popularity = popularity_range
        df = df.filter(
            (pl.col("Popularity") >= min_popularity)
            & (pl.col("Popularity") <= max_popularity)
        )

    if rating_range:
        min_rating, max_rating = rating_range
        df = df.filter(
            (pl.col("Rating") >= min_rating) & (pl.col("Rating") <= max_rating)
        )

    if nb_plays_range:
        min_nb_plays, max_nb_plays = nb_plays_range
        df = df.filter(
            (pl.col("NbPlays") >= min_nb_plays) & (pl.col("NbPlays") <= max_nb_plays)
        )

    if themes:
        df = df.filter(pl.col("Themes").str.contains("|".join(themes)))

    if opening_tags:
        df = df.filter(pl.col("OpeningTags").str.contains("|".join(opening_tags)))

    # Filter the puzzles by `max`, using the puzzles with the highest popularity scores
    # If two or more puzzles have the same popularity score, sort by the nb_plays column
    df = df.sort("Popularity", "NbPlays", descending=True).limit(max)
    df = df.collect()

    n_puzzles = len(df)

    if n_puzzles > 0:
        puzzle_pgns = []
        for pzl_row in progress.tqdm(
            df.iter_rows(), total=n_puzzles, desc="Fetching puzzles..."
        ):
            id = pzl_row[0]
            themes = pzl_row[7]
            opening_tags = pzl_row[9]
            fen = pzl_row[1]
            moves = pzl_row[2]
            pgn = generate_puzzle_db_pgn(id, fen, moves, themes)
            puzzle_pgns.append((pgn, themes))

        filename = "puzzles_db.csv"
        write_pgn_to_csv_with_tags(puzzle_pgns, filename=filename)
        download_info = f"Download CSV file with PGNs of {n_puzzles} puzzles"
        return df, gr.DownloadButton(
            value=filename,
            label=download_info,
            variant="primary",
            visible=True,
        )
    else:
        return df, gr.DownloadButton(
            label="No puzzles found. Please adjust the filters.",
            variant="secondary",
            visible=True,
        )
