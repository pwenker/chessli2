from datetime import date, datetime, timedelta
from pathlib import Path

import gradio as gr
from gradio_calendar import Calendar
from gradio_rangeslider import RangeSlider

from chessli2 import choices as ch
from chessli2.mistakes import validated_get_mistakes
from chessli2.tactics import get_puzzle_history, get_puzzles_from_db

readme_file = Path("README.md")
puzzle_themes_file = Path("docs/puzzle_themes.md")


with gr.Blocks(title="Chessli2") as chessli2_gradio_app:
    with gr.Tab("Welcome"):
        readme = readme_file.read_text()
        gr.Markdown(readme)

    with gr.Tab("Games & Mistakes"):
        gr.Markdown(
            """
            ### Learn from your Mistakes 💡✨
            
            Here you can fetch your games and mistakes from your **game history** 🎮. You can filter by time control, type of mistakes, and date range.
            
            When you are happy, you can download a CSV file with the selected mistakes' PGNs to practice them with Anki 📥.""",
        )

        user_name = gr.Textbox(
            label="User Name",
            placeholder="Enter your user name",
            info="Type in your lichess user name",
        )
        lichess_api_token_mistakes = gr.Textbox(
            placeholder="Paste your Lichess API key",
            label="Lichess API Token",
            lines=1,
            type="password",
        )
        with gr.Row():
            start_date = Calendar(
                type="datetime",
                value=datetime.now(),
                label="Select a start date",
                info="Click the calendar icon to bring up the calendar.",
            )
            end_date = Calendar(
                type="datetime",
                value=datetime.now(),
                label="Select an end date",
                info="Click the calendar icon to bring up the calendar.",
            )
        nags_checkbox = gr.CheckboxGroup(
            label="Mistake Types",
            value=[ch.MistakeNag.mistake.value, ch.MistakeNag.blunder.value],
            info="Select which types of mistakes should be detected",
            choices=[
                ("Mistake (?)", ch.MistakeNag.mistake.value),
                ("Blunder (??)", ch.MistakeNag.blunder.value),
                ("Speculative Move (!?)", ch.MistakeNag.speculative.value),
                ("Dubious Move (?!)", ch.MistakeNag.dubious.value),
            ],
        )
        time_control = gr.Dropdown(
            label="Filter by Time Control",
            value="All Time Controls",
            allow_custom_value=True,
            choices=[(tc.value, tc.name) for tc in ch.TimeControl],
        )
        get_mistakes_btn = gr.Button("Get Mistakes", variant="primary")

        mistake_pgns = gr.Textbox(visible=False)
        mistakes_md = gr.Markdown(label="Mistakes")

        mistakes_download_button = gr.DownloadButton(
            "Download CSV", variant="primary", visible=False
        )

    with gr.Tab("Puzzle History"):
        gr.Markdown(
            """
            ### Improve Tactics using your Puzzle History 🧩📈
            
            Here you can fetch your puzzles from your [puzzle history](https://lichess.org/training/history) 🧩.
            
            You can filter by [puzzle themes](https://lichess.org/training/themes) 🎯 and also select a maximum number of puzzles.
            When you are happy, you can download a CSV file with the selected puzzles' PGNs to practice them with Anki 📥."""
        )

        lichess_api_token_tactics = gr.Textbox(
            placeholder="Paste your Lichess API key",
            label="Lichess API Token",
            lines=1,
            type="password",
        )
        with gr.Accordion("Info about puzzle themes 🧩", open=False):
            gr.Markdown(puzzle_themes_file.read_text())

        puzzle_themes = gr.Dropdown(
            label="Puzzle Themes",
            info="Filter puzzles by selecting themes. Per default, all available themes are selected",
            multiselect=True,
            value=[th.name for th in ch.PuzzleTheme],
            choices=[(th.value, th.name) for th in ch.PuzzleTheme],
        )
        max_puzzles = gr.Slider(
            label="Maximum number of puzzles",
            info="Since Puzzle activity is sorted by reverse chronological order (most recent first), this selects the last n puzzles",
            minimum=1,
            value=100,
            maximum=100000,
        )
        until_date = Calendar(
            type="datetime",
            value=datetime.now() + timedelta(days=1),
            label="Only get puzzle activity before this time. Select time in future (default is 'tomorrow') to get whole puzzle activity.",
            info="Click the calendar icon to bring up the calendar.",
        )
        tactics_btn = gr.Button("Get tactics", variant="primary")
        puzzle_pgns = gr.Textbox(visible=False)
        puzzle_info = gr.JSON(label="Number of puzzles found organized by themes")
        puzzle_md_table = gr.Markdown()
        puzzle_download_button = gr.DownloadButton(
            "Download CSV", variant="primary", visible=False
        )
    with gr.Tab("Puzzle Database"):
        gr.Markdown(
            """
            ### Improve Tactics using the lichess Puzzle Database 🧩✨

            🕵️‍♂️ Fetch puzzles from the [lichess puzzle database](https://database.lichess.org/#puzzles), filter them by popularity, rating, number of plays, puzzle themes, and download them as CSV to practice with Anki 📊📚.
            """
        )
        popularity_range = RangeSlider(
            label="Popularity Range",
            minimum=-100,
            maximum=100,
            value=(80, 100),
            info="The popularity of the puzzle. Between 100 (best) and -100 (worst)",
        )
        rating_range = RangeSlider(
            label="Rating Range",
            minimum=0,
            maximum=4000,
            value=(0, 4000),
            info="The difficulty of the puzzle",
        )
        nb_plays_range = RangeSlider(
            label="Number of Plays Range",
            minimum=0,
            maximum=1007625,
            value=(0, 1007625),
            info="How often the puzzle was played",
        )
        puzzle_themes_cp = gr.Dropdown(
            label="Puzzle Themes",
            info="Filter puzzles by selecting themes. Per default, all available themes are selected",
            multiselect=True,
            value=[th.name for th in ch.PuzzleTheme],
            choices=[(th.value, th.name) for th in ch.PuzzleTheme],
        )
        opening_tags = gr.Dropdown(
            label="Opening Tags",
            value=None,
            choices=ch.opening_tags,
            visible=False,
            info="See: https://github.com/lichess-org/chess-openings",
        )
        puzzle_max = gr.Slider(
            label="Number of puzzles",
            minimum=1,
            maximum=10000,
            value=1000,
            info="Select the best puzzles (sorted by popularity & number of plays). You can either move the slider, or type in a number into the field.",
        )
        puzzle_db_btn = gr.Button("Fetch puzzles", variant="primary")
        puzzle_df = gr.DataFrame(
            headers=[
                "PuzzleId",
                "FEN",
                "Moves",
                "Rating",
                "RatingDeviation",
                "Popularity",
                "NbPlays",
                "Themes",
                "GameUrl",
                "OpeningTags",
            ]
        )
        puzzle_db_download_btn = gr.DownloadButton(
            "Download CSV", variant="primary", visible=False
        )
        puzzle_db_btn.click(
            get_puzzles_from_db,
            [
                puzzle_themes_cp,
                popularity_range,
                rating_range,
                nb_plays_range,
                opening_tags,
                puzzle_max,
            ],
            [puzzle_df, puzzle_db_download_btn],
        )

    # Event Handler
    get_mistakes_btn.click(
        fn=validated_get_mistakes,
        inputs=[
            lichess_api_token_mistakes,
            user_name,
            start_date,
            end_date,
            nags_checkbox,
            time_control,
        ],
        outputs=[mistake_pgns, mistakes_md, mistakes_download_button],
        api_name="get_mistakes",
    )
    tactics_btn.click(
        fn=get_puzzle_history,
        inputs=[until_date, max_puzzles, puzzle_themes, lichess_api_token_tactics],
        outputs=[puzzle_pgns, puzzle_info, puzzle_download_button],
    )

if __name__ == "__main__":
    chessli2_gradio_app.queue().launch()
