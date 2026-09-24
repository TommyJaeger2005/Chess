import tkinter as tk
from PIL import Image, ImageTk # type: ignore
from UI import UI
from Board import Board
import os

class Assets:
    # ----------------------------------------------
    #  DECLERATION AND RESIZE FOR ALL BLACK PIECES |
    # ----------------------------------------------

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PIECES_DIR = os.path.join(BASE_DIR, "Assets", "Pieces")

    pil_img = Image.open(os.path.join(PIECES_DIR,"black-pawn.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    BLACK_PAWN = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"black-rook.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    BLACK_ROOK = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"black-knight.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    BLACK_KNIGHT = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"black-bishop.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    BLACK_BISHOP = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"black-queen.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    BLACK_QUEEN = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"black-king.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    BLACK_KING= ImageTk.PhotoImage(resized_img)

    # ----------------------------------------------
    #  DECLERATION AND RESIZE FOR ALL WHITE PIECES |
    # ----------------------------------------------

    pil_img = Image.open(os.path.join(PIECES_DIR,"white-pawn.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    WHITE_PAWN = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"white-rook.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    WHITE_ROOK = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"white-knight.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    WHITE_KNIGHT = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"white-bishop.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    WHITE_BISHOP = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"white-queen.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    WHITE_QUEEN = ImageTk.PhotoImage(resized_img)

    pil_img = Image.open(os.path.join(PIECES_DIR,"white-king.png")).convert("RGBA")
    resized_img = pil_img.resize((90, 90), Image.Resampling.LANCZOS)
    WHITE_KING= ImageTk.PhotoImage(resized_img)

    # ------------------------------------------
    #  DECLERATION OF PIECE MAP FOR ALL PIECES |
    # ------------------------------------------
    PIECE_MAP = {
        1: WHITE_PAWN, 2: WHITE_ROOK, 3: WHITE_KNIGHT,
        4: WHITE_BISHOP, 5: WHITE_QUEEN, 6: WHITE_KING,
        -1: BLACK_PAWN, -2: BLACK_ROOK, -3: BLACK_KNIGHT,
        -4: BLACK_BISHOP, -5: BLACK_QUEEN, -6: BLACK_KING,
    }

    @staticmethod
    def CHECKMATE_POPUP():
        popup = tk.Toplevel(UI.GAME_FRAME)
        popup.title("GOOD GAME")
        popup.geometry("600x450")

        button_frame = tk.Frame(popup)
        button_frame.pack()

        pil_img = Image.open(os.path.join(Assets.BASE_DIR, "Assets", "CheckMate.png")).convert("RGBA")
        resized_img = pil_img.resize((600, 450), Image.Resampling.LANCZOS)
        CHECKMATE = ImageTk.PhotoImage(resized_img)

        btn = tk.Button(button_frame, image = CHECKMATE)
        btn.pack(side = "left", padx = 5)
        popup.button_images = CHECKMATE
        UI.GAME_FRAME.wait_window(popup)

    @staticmethod
    def STALEMATE_POPUP():
        popup = tk.Toplevel(UI.GAME_FRAME)
        popup.title("GOOD GAME")
        popup.geometry("750x400")

        button_frame = tk.Frame(popup)
        button_frame.pack()

        pil_img = Image.open(os.path.join(Assets.BASE_DIR, "Assets", "Stalemate.png")).convert("RGBA")
        resized_img = pil_img.resize((600, 450), Image.Resampling.LANCZOS)
        STALEMATE = ImageTk.PhotoImage(resized_img)

        btn = tk.Button(button_frame, image = STALEMATE)
        btn.pack(side = "left", padx = 5)
        popup.button_images = STALEMATE
        UI.GAME_FRAME.wait_window(popup)



    @staticmethod
    def PAWN_PROMOTION(row, col):
        from Logic import Logic
        popup = tk.Toplevel(UI.GAME_FRAME)
        popup.title("Pawn Promotion")
        popup.geometry("450x120")

        button_frame = tk.Frame(popup)
        button_frame.pack()
        prefix = "Black" if Logic.TURN > 0 else "White"

        options = {
            "queen":  5,
            "rook":   2,
            "bishop": 4,
            "knight": 3,
        }
        def MAKE_CHOICE(value):
            sign = 1 if prefix == "White" else -1
            Board.LOGICAL_BOARD[row][col] = sign * value
            popup.destroy()
            UI.REDRAW()
        
        button_images = []
        for value in options.items():
            img = Assets.PIECE_MAP[value if prefix == "White" else -value]
            btn = tk.Button(button_frame, image = img, command=lambda v = value: MAKE_CHOICE(v))
            btn.pack(side = "left", padx = 5)
            button_images.append(img)

        popup.button_images = button_images
        UI.GAME_FRAME.wait_window(popup)
