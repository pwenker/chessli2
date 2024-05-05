import io

import berserk
import chess.pgn
import gradio as gr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    lichess_api_token: str = ''


settings = Settings()

def generate_grid_html(games_list, row_length=2):
    game_ids = [
        chess.pgn.read_headers(io.StringIO(game_pgn))["Site"].rpartition("/")[-1]
        for game_pgn in games_list
    ]
    if row_length == 1:
        return "\n".join(
            [
                f'<iframe src="https://lichess.org/embed/game/{game_id}?theme=auto&bg=auto" width=600 height=397 frameborder=0></iframe>'
                for game_id in game_ids
            ]
        )
    else:
        html_rows = []
        for i in range(0, len(game_ids), row_length):
            row_html = "".join(
                [
                    f'<iframe src="https://lichess.org/embed/game/{id}?theme=auto&bg=auto" width="600" height="397" frameborder="0"></iframe>'
                    for id in game_ids[i : i + row_length]
                ]
            )
            # Wrap each row in a div for grid formatting
            html_rows.append(
                f'<div style="display: flex; justify-content: space-around;">{row_html}</div>'
            )
        return "\n".join(html_rows)

def fetch_games(
    user_name, start_date, end_date, lichess_api_token=settings.lichess_api_token
):
    gr.Info("Fetching chess games 🔄♟️")

    start = berserk.utils.to_millis(start_date)
    end = berserk.utils.to_millis(end_date)
    session = berserk.TokenSession(lichess_api_token)
    client = berserk.Client(session=session)
    games = client.games.export_by_player(
        user_name,
        as_pgn=True,
        color="black",
        evals=True,
        analysed=True,
        literate=True,
        since=start,
        until=end,
        opening=True,
    )
    games_list = list(games)


    game_ids_html = generate_grid_html(games_list)

    return games_list, gr.HTML(game_ids_html)
