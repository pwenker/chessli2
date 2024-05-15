# `chessli2`

**Usage**:

```console
$ chessli2 [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `mistakes`: Fetches mistakes from the API based on the...
* `puzzles`: Fetches puzzles from the API based on the...
* `serve`: Starts the app and serves it given...

## `chessli2 mistakes`

Fetches mistakes from the API based on the specified parameters.

**Usage**:

```console
$ chessli2 mistakes [OPTIONS]
```

**Options**:

* `--src TEXT`: Select either the name of the Hugging Face Space to load, (e.g. "pwenker/chessli2") or the full URL (including "http" or "https") of the hosted Gradio app to load (e.g. "http://localhost:7860/" or "https://bec81a83-5b5c-471e.gradio.live/  [default: pwenker/chessli2]
* `--lichess-api-token TEXT`: Select lichess API token  [default: your lichess API token in .env, e.g. lip_5tGPs3qUPcYoWpSnEZfH]
* `--user-name TEXT`: Select user name  [default: pwenker]
* `--start-date TEXT`: Select start date (YYYY-MM-DD)  [default: 2017-05-14]
* `--end-date TEXT`: Select end date (YYYY-MM-DD)  [default: 2024-05-14]
* `--nags INTEGER`: Filter by mistake nag type (blunder=4, mistake=2, speculative=5, dubious=6)  [default: 4, 2]
* `--time-control [Bullet|Blitz|Rapid|Classical|UltraBullet|All Time Controls]`: Filter by time control  [default: All Time Controls]
* `--output [file|info|pgn]`: Select whether to output mistakes as markdown table, as PGN string, or file path of CSV file containing PGNS  [default: file]
* `--help`: Show this message and exit.

## `chessli2 puzzles`

Fetches puzzles from the API based on the specified parameters.

**Usage**:

```console
$ chessli2 puzzles [OPTIONS]
```

**Options**:

* `--src TEXT`: Select either the name of the Hugging Face Space to load, (e.g. 'pwenker/chessli2') or the full URL (including 'http' or 'https') of the hosted Gradio app to load (e.g. 'http://localhost:7860/' or 'https://bec81a83-5b5c-471e.gradio.live/')  [default: http://pwenker.github.io/chessli2/]
* `--lichess-api-token TEXT`: Select lichess API token  [default: your lichess API token in .env, e.g. lip_5tGPs3qUPcYoWpSnEZfH]
* `--before TEXT`: Only get puzzle activity before this date (format YYYY-MM-DD)  [default: 2024-05-15]
* `--max INTEGER`: Select maxmimum number of puzzles  [default: 100]
* `--themes [Advanced pawn|Advantage|Anastasia's mate|Arabian mate|Attacking f2 or f7|Attraction|Back rank mate|Bishop endgame|Boden's mate|Castling|Capture the defender|Crushing|Double bishop mate|Dovetail mate|Equality|Kingside attack|Clearance|Defensive move|Deflection|Discovered attack|Double check|Endgame|Exposed king|Fork|Hanging piece|Hook mate|Interference|Intermezzo|Knight endgame|Long puzzle|Master games|Master vs Master games|Checkmate|Mate in 1|Mate in 2|Mate in 3|Mate in 4|Mate in 5 or more|Middlegame|One-move puzzle|Opening|Pawn endgame|Pin|Promotion|Queen endgame|Queen and Rook|Queenside attack|Quiet move|Rook endgame|Sacrifice|Short puzzle|Skewer|Smothered mate|Super GM games|Trapped piece|Underpromotion|Very long puzzle|X-Ray attack|Zugzwang|Healthy mix|Player games]`: Filter by puzzle themes  [default: Advanced pawn, Advantage, Anastasia's mate, Arabian mate, Attacking f2 or f7, Attraction, Back rank mate, Bishop endgame, Boden's mate, Castling, Capture the defender, Crushing, Double bishop mate, Dovetail mate, Equality, Kingside attack, Clearance, Defensive move, Deflection, Discovered attack, Double check, Endgame, Exposed king, Fork, Hanging piece, Hook mate, Interference, Intermezzo, Knight endgame, Long puzzle, Master games, Master vs Master games, Checkmate, Mate in 1, Mate in 2, Mate in 3, Mate in 4, Mate in 5 or more, Middlegame, One-move puzzle, Opening, Pawn endgame, Pin, Promotion, Queen endgame, Queen and Rook, Queenside attack, Quiet move, Rook endgame, Sacrifice, Short puzzle, Skewer, Smothered mate, Super GM games, Trapped piece, Underpromotion, Very long puzzle, X-Ray attack, Zugzwang, Healthy mix, Player games]
* `--output [file|info|pgn]`: Select whether to output info about mistakes, mistakes as PGN string, or a file path of CSV file containing PGNs  [default: file]
* `--help`: Show this message and exit.

## `chessli2 serve`

Starts the app and serves it given specified `server_name` and `server_port`.

**Usage**:

```console
$ chessli2 serve [OPTIONS]
```

**Options**:

* `--server-name TEXT`: To make app accessible on local network, set this to '0.0.0.0'. Can be set by environment variable GRADIO_SERVER_NAME. If None, will use '127.0.0.1  [default: 127.0.0.1]
* `--server-port INTEGER`: Will start gradio app on this port (if available). Can be set by environment variable GRADIO_SERVER_PORT. If None, will search for an available port starting at 7860.  [default: 7860]
* `--help`: Show this message and exit.
