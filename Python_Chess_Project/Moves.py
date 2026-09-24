from Board import Board
class Moves:

    # ----------------------------------------
    #  DECLERATION FOR PAWN PIECES MOVEMENTS |
    # ----------------------------------------

    @staticmethod
    def PAWN_MOVES(PAWN_COLOR, from_row, from_col, to_row, to_col):
        #CHECK IS IN BOUNDS
        direction = -1 if PAWN_COLOR > 0 else 1  # white moves up (-1), black moves down (1)

        if Board.IS_EN_PASSANT == True and to_row == Board.EN_PASSANT_ROW and to_col == Board.EN_PASSANT_COL and to_row == from_row + direction and abs(from_col - to_col) == 1:
                if Board.LOGICAL_BOARD[to_row][to_col] == 0:
                    return True

        # 1 square forward into empty square
        if to_row == from_row + direction and to_col == from_col:
            if Board.LOGICAL_BOARD[to_row][to_col] == 0:
                return True

        # diagonal capture
        if to_row == from_row + direction and abs(to_col - from_col) == 1:
            if Board.LOGICAL_BOARD[to_row][to_col] != 0:
                return True

        # 2 square first move
        start_row = 6 if PAWN_COLOR > 0 else 1  # white starts on row 6, black on row 1
        if from_row == start_row and to_row == from_row + (2 * direction) and to_col == from_col:
            if Board.LOGICAL_BOARD[to_row][to_col] == 0 and Board.LOGICAL_BOARD[from_row + direction][from_col] == 0:
                return True

        return False

    # ----------------------------------------
    #  DECLERATION FOR ROOK PIECES MOVEMENTS |
    # ----------------------------------------

    @staticmethod
    def ROOK_MOVES(ROOK_COLOR, from_row, from_col, to_row, to_col):
        # CHECK MOVEMENT IS DIAGONALLY
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        if row_diff != 0 and col_diff != 0:
            return False
    
        #CHECK IS IN BOUNDS
        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False
    
        # figure out which direction we're stepping
        row_step = (1 if row_diff > 0 else -1) if row_diff != 0 else 0
        col_step = (1 if col_diff > 0 else -1) if col_diff != 0 else 0

        # check for pieces blocking the path
        r, c = from_row + row_step, from_col + col_step
        while (r, c) != (to_row, to_col):
            if Board.LOGICAL_BOARD[r][c] != 0:
                return False
            r += row_step
            c += col_step
    
        target = Board.LOGICAL_BOARD[to_row][to_col]
        if target != 0 and (target > 0) == (ROOK_COLOR > 0):
            return False
    
        return True

    # ----------------------------------------
    #  DECLERATION FOR KNIGHT PIECES MOVEMENTS |
    # ----------------------------------------

    @staticmethod
    def KNIGHT_MOVES(KNIGHT_COLOR, from_row, from_col, to_row, to_col):
        possible = [
            (from_row + 2, from_col + 1),
            (from_row + 2, from_col - 1),
            (from_row - 2, from_col + 1),
            (from_row - 2, from_col - 1),
            (from_row + 1, from_col + 2),
            (from_row + 1, from_col - 2),
            (from_row - 1, from_col + 2),
            (from_row - 1, from_col - 2),
        ]
        #CHECK IS IN BOUNDS
        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False
    
        if (to_row, to_col) not in possible:
            return False
    
        target = Board.LOGICAL_BOARD[to_row][to_col]
        if target != 0 and (target > 0) == (KNIGHT_COLOR > 0):
            return False
    
        return True

    # ------------------------------------------
    #  DECLERATION FOR BISHOP PIECES MOVEMENTS |
    # ------------------------------------------

    @staticmethod
    def BISHOP_MOVES(BISHOP_COLOR, from_row, from_col, to_row, to_col):
    # CHECK MOVEMENT IS NOT DIAGONALLY
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        if abs(row_diff) != abs(col_diff):
            return False
    
        #CHECK IS IN BOUNDS
        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False
    
        # check for pieces blocking the path
        row_step = 1 if row_diff > 0 else -1
        col_step = 1 if col_diff > 0 else -1
        r, c = from_row + row_step, from_col + col_step

        while (r, c) != (to_row, to_col):
            if Board.LOGICAL_BOARD[r][c] != 0:
                return False  # something is in the way
        
            r += row_step
            c += col_step
    
        target = Board.LOGICAL_BOARD[to_row][to_col]
        if target != 0 and (target > 0) == (BISHOP_COLOR > 0):
            return False
    
        return True

    # ----------------------------------------
    #  DECLERATION FOR QUEEN PIECES MOVEMENTS |
    # ----------------------------------------

    @staticmethod
    def QUEEN_MOVES(QUEEN_COLOR, from_row, from_col, to_row, to_col):
        return Moves.BISHOP_MOVES(QUEEN_COLOR, from_row, from_col, to_row, to_col) or Moves.ROOK_MOVES(QUEEN_COLOR, from_row, from_col, to_row, to_col)

    # ----------------------------------------
    #  DECLERATION FOR KING PIECES MOVEMENTS |
    # ----------------------------------------

    @staticmethod
    def KING_MOVES(KING_COLOR, from_row, from_col, to_row, to_col):
        possible = [
            (from_row + 1, from_col),
            (from_row - 1, from_col),
            (from_row, from_col + 1),
            (from_row, from_col - 1),
            (from_row + 1, from_col + 1),
            (from_row + 1, from_col - 1),
            (from_row - 1, from_col + 1),
            (from_row - 1, from_col - 1),
        ]
        #CHECK IS IN BOUNDS
        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False
    
        if (to_row, to_col) not in possible:
            return False
    
    
        target = Board.LOGICAL_BOARD[to_row][to_col]
        if target != 0 and (target > 0) == (KING_COLOR > 0):
            return False
        
        return True