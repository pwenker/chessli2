import csv
import pandas as pd
import chess
from io import StringIO
import gradio as gr


def write_pgn_to_csv(pgns, filename="pgns.csv"):
    """
    Writes a list of PGN strings to a CSV file with a single header 'PGN'.

    Args:
    pgns (list of str): List containing PGN strings.
    filename (str): Name of the CSV file to be created.
    """
    # Open the file in write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write each PGN as a new row
        for pgn in pgns:
            writer.writerow([pgn])

def write_pgn_to_csv_with_tags(pgns, filename="pgns.csv"):
    # Open the file in write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write each PGN as a new row
        for pgn, tags in pgns:
            writer.writerow([pgn, tags])

def mistake_pgns_to_md(mistake_pgns):
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
            "Time Control": headers['TimeControl'],
            "Mistake ❌": mistake,
            "Correct Variation ✅": correct_variation,
        }

    df = pd.DataFrame(data=mistake_pgns, columns=["PGN"])
    df_info = df["PGN"].apply(parse_pgn).apply(pd.Series)

    return df_info.to_markdown(index=False)
