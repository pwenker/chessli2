from enum import Enum


class Output(str, Enum):
    file = "file"
    info = "info"
    pgn = "pgn"


class Color(Enum):
    white = 1
    black = 0


class MistakeNag(Enum):
    mistake = 2
    blunder = 4
    speculative = 5
    dubious = 6


class TimeControl(str, Enum):
    bullet = "Bullet"
    blitz = "Blitz"
    rapid = "Rapid"
    classical = "Classical"
    ultraBullet = "UltraBullet"
    all = "All Time Controls"


class PuzzleTheme(str, Enum):
    advancedPawn = "Advanced pawn"
    advantage = "Advantage"
    anastasiaMate = "Anastasia's mate"
    arabianMate = "Arabian mate"
    attackingF2F7 = "Attacking f2 or f7"
    attraction = "Attraction"
    backRankMate = "Back rank mate"
    bishopEndgame = "Bishop endgame"
    bodenMate = "Boden's mate"
    castling = "Castling"
    capturingDefender = "Capture the defender"
    crushing = "Crushing"
    doubleBishopMate = "Double bishop mate"
    dovetailMate = "Dovetail mate"
    equality = "Equality"
    kingsideAttack = "Kingside attack"
    clearance = "Clearance"
    defensiveMove = "Defensive move"
    deflection = "Deflection"
    discoveredAttack = "Discovered attack"
    doubleCheck = "Double check"
    endgame = "Endgame"
    exposedKing = "Exposed king"
    fork = "Fork"
    hangingPiece = "Hanging piece"
    hookMate = "Hook mate"
    interference = "Interference"
    intermezzo = "Intermezzo"
    knightEndgame = "Knight endgame"
    long = "Long puzzle"
    master = "Master games"
    masterVsMaster = "Master vs Master games"
    mate = "Checkmate"
    mateIn1 = "Mate in 1"
    mateIn2 = "Mate in 2"
    mateIn3 = "Mate in 3"
    mateIn4 = "Mate in 4"
    mateIn5 = "Mate in 5 or more"
    middlegame = "Middlegame"
    oneMove = "One-move puzzle"
    opening = "Opening"
    pawnEndgame = "Pawn endgame"
    pin = "Pin"
    promotion = "Promotion"
    queenEndgame = "Queen endgame"
    queenRookEndgame = "Queen and Rook"
    queensideAttack = "Queenside attack"
    quietMove = "Quiet move"
    rookEndgame = "Rook endgame"
    sacrifice = "Sacrifice"
    short = "Short puzzle"
    skewer = "Skewer"
    smotheredMate = "Smothered mate"
    superGM = "Super GM games"
    trappedPiece = "Trapped piece"
    underPromotion = "Underpromotion"
    veryLong = "Very long puzzle"
    xRayAttack = "X-Ray attack"
    zugzwang = "Zugzwang"
    healthyMix = "Healthy mix"
    playerGames = "Player games"
