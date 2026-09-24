import tkinter as tk
from PIL import Image, ImageTk # type: ignore
from Board import Board

class UI:
    TILE_SIZE = 100
    COLORS = ["#eeeed2", "#769656"]

    # --------------------------------------------------------------------
    #  DECLERATION OF THE FRAME THE CHESS BOARD AND THE PICES WILL BE ON |
    # --------------------------------------------------------------------

    GAME_FRAME = tk.Tk()
    GAME_FRAME.title("Lets Make Chess!")
    GAME_FRAME.geometry("900x900")

    # -----------------------------
    #  DECLERATION OF THE CANVAS  |
    # -----------------------------

    CHESS_BOARD = tk.Canvas(GAME_FRAME, height = 800, width = 800)
    CHESS_BOARD.place(anchor = tk.CENTER)
    CHESS_BOARD.grid()

    @staticmethod
    def DRAW_BOARD():
        for row in range(8):
            for col in range(8):
                color = UI.COLORS[(row + col) % 2]
                x1 = col * UI.TILE_SIZE
                y1 = row * UI.TILE_SIZE
                x2 = x1 + UI.TILE_SIZE
                y2 = y1 + UI.TILE_SIZE
                UI.CHESS_BOARD.create_rectangle(x1, y1, x2, y2, fill = color, outline = "BLACK")

    # -----------------------------------------------------
    #  DECLERATION OF FUNCTION TO REDRAW BOARD AFTER MOVE |
    # -----------------------------------------------------
    
    @staticmethod
    def REDRAW():
        from Assets import Assets
        UI.DRAW_BOARD()  # redraw squares first
        for row in range(8):
            for col in range(8):
                piece = Board.LOGICAL_BOARD[row][col]
                if piece != 0:
                    x = col * UI.TILE_SIZE + 5
                    y = row * UI.TILE_SIZE + 5
                    UI.CHESS_BOARD.create_image(x, y, anchor="nw", image = Assets.PIECE_MAP[piece])