import io
from enum import Enum

import chess
import chess.pgn
import gradio as gr

from chessli2.games import fetch_games


class Color(Enum):
    white = 1
    black = 0


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


def get_mistakes(lichess_api_token, user_name, start_date, end_date, nags):
    games, _ = fetch_games(user_name, start_date, end_date, lichess_api_token)

    gr.Info("Finding mistakes 🔍❌")
    mistake_pgns = []
    for game_pgn in games:
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
            
    return [[mp] for mp in mistake_pgns]


def validate_user_input(user_name, start_date, end_date):
    if not user_name.strip():
        raise gr.Error("User name cannot be empty.")
    if start_date > end_date:
        raise gr.Error("Start date must be before end date.")
    return user_name, start_date, end_date


def validated_get_mistakes(lichess_api_token, user_name, start_date, end_date, nags):
    user_name, start_date, end_date = validate_user_input(
        user_name, start_date, end_date
    )
    return get_mistakes(lichess_api_token, user_name, start_date, end_date, nags)
