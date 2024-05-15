import io

import berserk
import chess
import chess.pgn
import gradio as gr

from chessli2.choices import Color
from chessli2.settings import get_client
from chessli2.writer import mistake_pgns_to_md, write_pgn_to_csv


def create_mistake_pgn(game_node):
    parent = game_node.parent
    game_root = game_node.game()

    mistake_pgn = chess.pgn.Game()
    mistake_pgn.headers = game_root.headers.copy()
    mistake_pgn.setup(parent.parent.board())

    mainline, *variations = parent.variations
    assert len(variations) == 1
    assert mainline.is_mainline()

    vr = variations[0]

    moves = [vr.parent.move, vr.move, *[n.move for n in vr.mainline()]]
    mistake_pgn.add_line(
        moves=moves,
        starting_comment=f"{game_node.comment} (player's move was {game_node.san()})",
    )

    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
    pgn_string = mistake_pgn.accept(exporter)
    return pgn_string


def get_mistakes(
    lichess_api_token, user_name, start_date, end_date, nags, time_control
):
    client, lichess_api_token = get_client(lichess_api_token=lichess_api_token)

    if not lichess_api_token:
        gr.Info(
            "If you authenticate with your lichess API token you can increase requests limit from 20 to 60 games per second!"
        )

    games = client.games.export_by_player(
        user_name,
        as_pgn=True,
        evals=True,
        analysed=True,
        literate=True,
        since=berserk.utils.to_millis(start_date),
        perf_type=None if time_control == "all" else time_control,
        until=berserk.utils.to_millis(end_date),
        opening=True,
    )

    mistake_pgns = []
    n_games = 0
    try:
        for n, game_pgn in enumerate(games):
            game_pgn = io.StringIO(game_pgn)
            game_node = chess.pgn.read_game(game_pgn)

            player: Color = (
                Color.white if game_node.headers["White"] == user_name else Color.black
            )

            def was_players_move(game_node):
                return player.value != game_node.turn()

            def relevant_mistakes_were_made(game_node, nags):
                return game_node.nags and game_node.nags.issubset(set(nags))

            while game_node is not None:
                if was_players_move(game_node) and relevant_mistakes_were_made(
                    game_node, nags
                ):
                    mistake_pgn = create_mistake_pgn(game_node)

                    mistake_pgns.append(mistake_pgn)
                game_node = game_node.next()

            n_games = n
            info = f"Fetched {n} games(s) with {len(mistake_pgns)} mistakes..."
            yield mistake_pgns, "", gr.DownloadButton(
                label=info, variant="secondary", visible=True
            )

        if mistake_pgns:
            filename = f"{user_name}_mistakes.csv"
            write_pgn_to_csv(mistake_pgns, filename=filename)
            mistakes_md = mistake_pgns_to_md(mistake_pgns=mistake_pgns)
            info = f"Download CSV file with PGNs of {len(mistake_pgns)} mistakes in {n_games} games"
            yield mistake_pgns, mistakes_md, gr.DownloadButton(
                value=filename, label=info, variant="primary"
            )
        else:
            mistakes_md = ""
            yield mistake_pgns, mistakes_md, gr.DownloadButton(
                label="No mistakes found", variant="secondary"
            )
    except berserk.exceptions.ResponseError:
        gr.Warning("Your lichess API token is invalid. Did you misspell it?")
        yield "", "", gr.DownloadButton(
            label="Please insert a correct lichess API token into the textbox at the top of the interface or leave it empty",
            visible=True,
            variant="stop",
        )


def validate_user_input(user_name, start_date, end_date):
    if not user_name.strip():
        raise gr.Error("User name cannot be empty.")
    if start_date > end_date:
        raise gr.Error("Start date must be before end date.")
    return user_name, start_date, end_date


def validated_get_mistakes(
    lichess_api_token, user_name, start_date, end_date, nags, time_control
):
    user_name, start_date, end_date = validate_user_input(
        user_name, start_date, end_date
    )
    yield from get_mistakes(
        lichess_api_token, user_name, start_date, end_date, nags, time_control
    )
