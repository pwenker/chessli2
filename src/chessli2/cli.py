import logging

import typer
from gradio_client import Client
from rich import print

from chessli2.choices import MistakeNag, Output, PuzzleTheme, TimeControl
from chessli2.settings import settings

app = typer.Typer()


@app.command()
def serve(
    server_name: str = typer.Option(
        "127.0.0.1",
        help="To make app accessible on local network, set this to '0.0.0.0'. Can be set by environment variable GRADIO_SERVER_NAME. If None, will use '127.0.0.1",
    ),
    server_port: int = typer.Option(
        7860,
        help="Will start gradio app on this port (if available). Can be set by environment variable GRADIO_SERVER_PORT. If None, will search for an available port starting at 7860.",
    ),
):
    """
    Starts the app and serves it given specified `server_name` and `server_port`.
    """
    from chessli2.gui import chessli2_gradio_app

    chessli2_gradio_app.launch(server_port=server_port, server_name=server_name)


@app.command()
def mistakes(
    src: str = typer.Option(
        "pwenker/chessli2",
        help='Select either the name of the Hugging Face Space to load, (e.g. "pwenker/chessli2") or the full URL (including "http" or "https") of the hosted Gradio app to load (e.g. "http://localhost:7860/" or "https://bec81a83-5b5c-471e.gradio.live/',
    ),
    lichess_api_token: str = typer.Option(
        settings.lichess_api_token, help="Select lichess API token"
    ),
    user_name: str = typer.Option("pwenker", help="Select user name"),
    start_date: str = typer.Option("2017-05-14", help="Select start date (YYYY-MM-DD)"),
    end_date: str = typer.Option("2024-05-14", help="Select end date (YYYY-MM-DD)"),
    nags: list[int] = typer.Option(
        [MistakeNag.blunder.value, MistakeNag.mistake.value],
        help="Filter by mistake nag type (blunder=4, mistake=2, speculative=5, dubious=6)",
    ),
    time_control: TimeControl = typer.Option(
        TimeControl.all, help="Filter by time control"
    ),
    output: Output = typer.Option(
        Output.file,
        help="""Select whether to output mistakes as markdown table, as PGN string, or file path of CSV file containing PGNS""",
    ),
):
    """
    Fetches mistakes from the API based on the specified parameters.
    """
    client = Client(src)
    mistake_pgns, mistake_md, mistake_csv = client.predict(
        lichess_api_token=lichess_api_token,
        user_name=user_name,
        start_date=start_date,
        end_date=end_date,
        nags=nags,
        time_control=time_control,
        api_name="/get_mistakes",
    )

    if output == Output.info:
        print(mistake_md)
    elif output == Output.pgn:
        print(mistake_pgns)
    elif output == Output.file:
        print(mistake_csv["value"])


@app.command()
def puzzles(
    src: str = typer.Option(
        "http://pwenker.github.io/chessli2/",
        help="Select either the name of the Hugging Face Space to load, (e.g. 'pwenker/chessli2') or the full URL (including 'http' or 'https') of the hosted Gradio app to load (e.g. 'http://localhost:7860/' or 'https://bec81a83-5b5c-471e.gradio.live/')",
    ),
    lichess_api_token: str = typer.Option(
        settings.lichess_api_token, help="Select lichess API token"
    ),
    before: str = typer.Option(
        "2024-05-15",
        help="Only get puzzle activity before this date (format YYYY-MM-DD)",
    ),
    max: int = typer.Option(100, help="Select maxmimum number of puzzles"),
    themes: list[PuzzleTheme] = typer.Option(
        [pt for pt in PuzzleTheme],
        help="Filter by puzzle themes",
    ),
    output: Output = typer.Option(
        Output.file,
        help="Select whether to output info about mistakes, mistakes as PGN string, or a file path of CSV file containing PGNs",
    ),
):
    """
    Fetches puzzles from the API based on the specified parameters.
    """
    logging.disable(logging.CRITICAL)
    client = Client(src)
    puzzle_pgns, puzzle_theme_counter, puzzle_csv = client.predict(
        before=before,
        max=max,
        themes_selection=themes,
        api_name="/get_puzzles",
    )

    if output == Output.info:
        print(puzzle_theme_counter)
    elif output == Output.pgn:
        print(puzzle_pgns)
    elif output == Output.file:
        print(puzzle_csv["value"])


if __name__ == "__main__":
    app()
