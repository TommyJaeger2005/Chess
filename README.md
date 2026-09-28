# Python Chess

A simple two-player chess game built with Python and Tkinter.

<img width="892" height="869" alt="Screenshot 2026-09-28 at 11 23 23 AM" src="https://github.com/user-attachments/assets/53879464-a9b1-4d41-8445-3b22a2b6364e" />


## Features

- Full legal move validation for all pieces
- Castling, including all rules and restrictions
- En passant capture
- Pawn promotion (queen, rook, bishop, knight)
- Check, checkmate, and stalemate detection
- Click-to-move interface

## Requirements

- Python 3.10+
- Pillow (`pip install Pillow`)

## Setup

```bash
git clone https://github.com/TommyJaeger2005/Chess.git
cd Chess/Python_Chess_Project
pip install Pillow
```

## Running the game

```bash
python3 Main.py
```

## How to play

Click a piece to select it, then click a destination square to move it.
Pawn promotion and check/checkmate/stalemate are handled automatically with popups.

## Project structure

| File | Purpose |
|---|---|
| `Main.py` | starts the game window |
| `Board.py` | Holds the board state |
| `Logic.py` | Turn handling, click events, check/checkmate detection |
| `Moves.py` | Legal move rules for each piece |
| `UI.py` | Drawing the board and pieces |
| `Assets.py` | Loads piece images and popup windows |

## Known limitations

- No move history / undo
- No draw by repetition or 50-move rule
- No AI opponent (two-player local only)
