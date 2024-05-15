import datetime
from collections import Counter

import berserk
import chess
import gradio as gr

from chessli2.settings import get_client
from chessli2.writer import write_pgn_to_csv


def puzzle_pgn(puzzle_activity):
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


def get_puzzles(before, max, themes_selection, lichess_api_token):
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
            ppgn, themes = puzzle_pgn(client.puzzles.get(pa["puzzle"]["id"]))
            # check if any of the selected themes are in the puzzle themes
            if not set(themes_selection).isdisjoint(themes):
                n_puzzles += 1
                theme_counter.update(themes)
                puzzle_pgns.append(ppgn)
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
            write_pgn_to_csv(puzzle_pgns, filename=filename)
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


def create_markdown_table(entries):
    if not entries:
        return "No data provided"

    if not isinstance(entries, list) or not all(
        isinstance(item, dict) for item in entries
    ):
        return "Invalid input format. Please provide a list of dictionaries."

    # Extract headers from the first dictionary
    headers = entries[0].keys()

    # Create the header row
    header_row = "| " + " | ".join(headers) + " |"

    # Create the separator row
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"

    # Initialize the table with the header and separator
    table = [header_row, separator_row]

    # Fill in the data rows
    for entry in entries:
        row = []
        for header in headers:
            if header in entry:
                value = entry[header]
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S %Z")
                elif isinstance(value, list):
                    value = ", ".join(map(str, value))
                row.append(str(value))
            else:
                row.append("N/A")
        table.append("| " + " | ".join(row) + " |")

    return "\n".join(table)
