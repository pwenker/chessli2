import pytest
from typer.testing import CliRunner

from chessli2.cli import app
from chessli2.settings import settings

runner = CliRunner()

sources = ["pwenker/chessli2", "http://localhost:7860"]


@pytest.mark.parametrize("src", ["http://localhost:7860"])
def test_mistakes_with_options(src):
    result = runner.invoke(
        app,
        [
            "mistakes",
            "--src",
            src,
            "--lichess-api-token",
            settings.lichess_api_token,
            "--user-name",
            "pwenker",
            "--start-date",
            "2017-05-14",
            "--end-date",
            "2024-05-14",
            "--nags",
            "4",
            "--nags",
            "2",
            "--time-control",
            "All Time Controls",
            "--output",
            "file",
        ],
    )
    assert result.exit_code == 0


@pytest.mark.parametrize("src", ["http://localhost:7860"])
def test_puzzles_with_options(src):
    """
    chessli puzzles --src http://localhost:7860  --user-name pwenker --before 2024-05-14 --max 100 --output file
    """
    result = runner.invoke(
        app,
        [
            "puzzles",
            "--src",
            src,
            "--lichess-api-token",
            settings.lichess_api_token,
            "--before",
            "2024-05-14",
            "--max",
            '10',
            "--output",
            "file",
        ],
    )
    __import__('pdb').set_trace()
    assert result.exit_code == 0
