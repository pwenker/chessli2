from datetime import datetime
from io import StringIO
from pathlib import Path

import chess.pgn
import gradio as gr
import pandas as pd
from gradio_calendar import Calendar

from src.chessli2.mistakes import validated_get_mistakes

readme_file = Path("README.md")

nags = {
    "Mistake (?)": 2,
    "Blunder (??)": 4,
    "Speculative Move (!?)": 5,
    "Dubious Move (?!)": 6,
}

with gr.Blocks() as demo:
    with gr.Tab("Welcome"):
        gr.Markdown(readme_file.read_text())
    with gr.Tab("Games & Mistakes"):
        gr.Markdown("Fetch your games and download a CSV with your mistakes")

        lichess_api_token = gr.Textbox(
            placeholder="Paste your Lichess API key",
            label="Lichess API Token",
            lines=1,
            type="password",
        )
        user_name = gr.Textbox(
            label="User Name",
            placeholder="Enter your user name",
            info="Type in your lichess user name",
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
            value=[2, 4],  # Mistakes and Blundes per default
            info="Select which types of mistakes should be detected",
            choices=[(k, v) for k, v in nags.items()],
        )
        get_mistakes_btn = gr.Button("Get Mistakes", variant="primary")

        gr.Markdown("### Mistakes")
        mistakes_df = gr.Dataframe(
            headers=["PGN"],
            visible=False,
            interactive=False,
        )
        mistakes_md = gr.Markdown()

        def export_csv(df, user_name):
            gr.Info("Preparing downloadable CSV file 💾")
            file_name = f"mistakes_{user_name}.csv"
            df.to_csv(
                file_name,
                index=False,
                header=False,
            )
            return gr.DownloadButton(value=file_name, visible=True)

        download_button = gr.DownloadButton(
            "Download CSV", variant="primary", visible=False
        )

        def df_to_md(df):
            gr.Info("Visualizing mistakes as markdown table 📉📝")

            def parse_pgn(pgn_text):
                pgn_io = StringIO(pgn_text)
                game = chess.pgn.read_game(pgn_io)
                headers = game.headers
                moves = pgn_text.split("\n\n")[1]
                mistake, *correct_variation = moves.split("\n")
                result_emoji = (
                    "✅"
                    if headers["Result"] == "1-0"
                    else "❌"
                    if headers["Result"] == "0-1"
                    else "➖"
                )
                return {
                    "White": headers["White"],
                    "Black": headers["Black"],
                    "Result": result_emoji,
                    "White Elo": headers["WhiteElo"],
                    "Black Elo": headers["BlackElo"],
                    "Opening": headers["Opening"],
                    "Mistake ❌": mistake,
                    "Correct Variation ✅": correct_variation,
                }

            df_info = df["PGN"].apply(parse_pgn).apply(pd.Series)

            return df_info.to_markdown(index=False)

        get_mistakes_btn.click(
            fn=validated_get_mistakes,
            inputs=[lichess_api_token, user_name, start_date, end_date, nags_checkbox],
            outputs=mistakes_df,
            api_name="get_mistakes",
        ).success(
            fn=export_csv,
            inputs=[mistakes_df, user_name],
            outputs=download_button,
        ).success(
            fn=df_to_md,
            inputs=mistakes_df,
            outputs=mistakes_md,
        )
