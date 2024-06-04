import shutil
from pathlib import Path

from gradio_client import Client
from tqdm import tqdm

themes = [
    "advancedPawn",
    "advantage",
    "anastasiaMate",
    "arabianMate",
    "attackingF2F7",
    "attraction",
    "backRankMate",
    "bishopEndgame",
    "bodenMate",
    "castling",
    "capturingDefender",
    "crushing",
    "doubleBishopMate",
    "dovetailMate",
    "equality",
    "kingsideAttack",
    "clearance",
    "defensiveMove",
    "deflection",
    "discoveredAttack",
    "doubleCheck",
    "endgame",
    "exposedKing",
    "fork",
    "hangingPiece",
    "hookMate",
    "interference",
    "intermezzo",
    "knightEndgame",
    "long",
    "master",
    "masterVsMaster",
    "mate",
    "mateIn1",
    "mateIn2",
    "mateIn3",
    "mateIn4",
    "mateIn5",
    "middlegame",
    "oneMove",
    "opening",
    "pawnEndgame",
    "pin",
    "promotion",
    "queenEndgame",
    "queenRookEndgame",
    "queensideAttack",
    "quietMove",
    "rookEndgame",
    "sacrifice",
    "short",
    "skewer",
    "smotheredMate",
    "superGM",
    "trappedPiece",
    "underPromotion",
    "veryLong",
    "xRayAttack",
    "zugzwang",
    "healthyMix",
    "playerGames",
]
client = Client("http://localhost:7860/")


for theme in tqdm(themes, desc="Generating puzzles...", total=len(themes)):
    csv_data, csv_file = client.predict(
        themes=[theme],
        popularity_range=[80, 100],
        rating_range=[0, 4000],
        nb_plays_range=[0, 1007625],
        opening_tags=None,
        max=1000,
        api_name="/get_puzzles_from_db",
    )

    src = csv_file["value"]
    dest = f"puzzles/{theme}.csv"

    shutil.copy(Path(src), dest)
