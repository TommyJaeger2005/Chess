from Board import Board
from Assets import Assets
from UI import UI
from Moves import Moves

class Logic:

    SELECTED = None
    TURN = 1 # 1 for WHITE -1 for BLACK

    @staticmethod
    def ON_CLICK(event):

        direction = -1 if Logic.TURN > 0 else 1
        col = event.x // 100
        row = event.y // 100

        if Logic.SELECTED is None:
            piece = Board.LOGICAL_BOARD[row][col] #GET PIECE VALUE TO CHECK WHITE OR BLACK
            if Board.LOGICAL_BOARD[row][col] != 0 and (piece > 0) == (Logic.TURN > 0):
                Logic.SELECTED = (row, col)
    
        else:
            from_row, from_col = Logic.SELECTED
            piece = Board.LOGICAL_BOARD[from_row][from_col]
            IS_EN_PASSANT_CAPTURE = False

            TARGET = Board.LOGICAL_BOARD[row][col] #CHECK THE GOAL POSITION TO MOVE TOO

            IS_CASTLE = False

            if(abs(piece) == 6 and abs(TARGET) == 2):
                IS_CASTLE = True

            if(abs(piece) == 1 and TARGET == 0 and abs(from_col - col) == 1):
                IS_EN_PASSANT_CAPTURE = True

            if TARGET == 0 or (TARGET > 0) != (Logic.TURN > 0) or IS_CASTLE: #CHECKS IF SPACE IS EMPTY OR THE OCCUPYING PIECE IS OF DIFFRENT COLOR
                if Logic.IS_VALID_MOVE(from_row, from_col, row, col):
                    saved_target = Board.LOGICAL_BOARD[row][col]
                    EN_PASSANT_Target = 0
                    Saved_King = Board.LOGICAL_BOARD[from_row][from_col]
                    Saved_Rook = saved_target

                    if IS_CASTLE:

                        IS_LEFT = False #IS THE CASTLING TO THE LEFT OR RIGHT
                        if(col < 4):
                             IS_LEFT = True

                        #START CASTLE MOVE
                        Board.LOGICAL_BOARD[from_row][from_col] = 0
                        Board.LOGICAL_BOARD[row][col] = 0
                        if(IS_LEFT):
                            Board.LOGICAL_BOARD[row][from_col - 2] = Saved_King
                            Board.LOGICAL_BOARD[row][from_col - 1] = Saved_Rook
                        else:
                            Board.LOGICAL_BOARD[row][from_col + 2] = Saved_King
                            Board.LOGICAL_BOARD[row][from_col + 1] = Saved_Rook
                        #END CASTLE MOVE
                
                    if not IS_CASTLE:
                        Board.LOGICAL_BOARD[row][col] = Board.LOGICAL_BOARD[from_row][from_col]
                        Board.LOGICAL_BOARD[from_row][from_col] = 0

                        if IS_EN_PASSANT_CAPTURE:
                            EN_PASSANT_Target = Board.LOGICAL_BOARD[from_row][Board.EN_PASSANT_COL]
                            Board.LOGICAL_BOARD[from_row][Board.EN_PASSANT_COL]  = 0

                    if Logic.IS_CHECK(Logic.TURN): #START REVERT FOR MOVE ENDING IN CHECK
                        if IS_CASTLE:
                            Board.LOGICAL_BOARD[from_row][from_col] = Saved_King
                            Board.LOGICAL_BOARD[row][col] = Saved_Rook

                            IS_LEFT = False #IS THE CASTLING TO THE LEFT OR RIGHT
                            if(col < 4):
                                IS_LEFT = True
                            if(IS_LEFT):
                                Board.LOGICAL_BOARD[row][from_col - 2] = 0
                                Board.LOGICAL_BOARD[row][from_col - 1] = 0
                            else:
                                Board.LOGICAL_BOARD[row][from_col + 2] = 0
                                Board.LOGICAL_BOARD[row][from_col + 1] = 0

                        else: #IF THE MOVE RESULTING IN CHECK WAS NOT CASTLING
                            Board.LOGICAL_BOARD[from_row][from_col] = Board.LOGICAL_BOARD[row][col]
                            Board.LOGICAL_BOARD[row][col] = saved_target

                            if IS_EN_PASSANT_CAPTURE:
                                Board.LOGICAL_BOARD[from_row][Board.EN_PASSANT_COL] = EN_PASSANT_Target

                        Logic.SELECTED = (row, col)

                    else:
                        Logic.TURN *= -1 #SWITCHES TURNS
                        Logic.SELECTED = None

                        if IS_CASTLE:
                            if(Saved_King > 0):
                                Board.WHITE_KING_MOVED = True
                            else:
                                Board.BLACK_KING_MOVED = True
                    
                        if(abs(piece) == 1 and abs(from_row - row) == 2):
                            Board.EN_PASSANT_ROW = row - direction
                            Board.EN_PASSANT_COL = col
                            Board.IS_EN_PASSANT = True
                        else:
                            Board.IS_EN_PASSANT = False


                        no_legal_moves = Logic.IS_CHECKMATE()

                        if Logic.IS_CHECK(Logic.TURN):  # is the NEW player now in check?
                            if no_legal_moves:
                                print("CHECKMATE")
                                Assets.CHECKMATE_POPUP()
                        else:
                            if no_legal_moves: #If THERE IS NO PRIOR CHECK THEN ITS STALEMATE:
                                print("STALEMATE")
                                Assets.STALEMATE_POPUP()

                        if Board.LOGICAL_BOARD[row][col] == 1 and row == 0:
                            Assets.PAWN_PROMOTION(row, col)
                        elif Board.LOGICAL_BOARD[row][col] == -1 and row == 7:
                            Assets.PAWN_PROMOTION(row, col)

                        UI.REDRAW()
            else:
                Logic.SELECTED = (row, col) #CASE WHERE SELECTION DOES NOT MEET CRITERA

    @staticmethod
    def IS_VALID_MOVE(from_row, from_col, to_row, to_col):
        PIECE_COLOR = Board.LOGICAL_BOARD[from_row][from_col] 
        piece = abs(Board.LOGICAL_BOARD[from_row][from_col]) #MAKES ALL PIECES POSITIVE TO HAVE LESS FUNCTIONS REQUIRED
        if piece == 1: return Moves.PAWN_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
        if piece == 2: return Moves.ROOK_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
        if piece == 3: return Moves.KNIGHT_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
        if piece == 4: return Moves.BISHOP_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
        if piece == 5: return Moves.QUEEN_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
        if piece == 6:
            if(abs(Board.LOGICAL_BOARD[to_row][to_col]) == 2):
                return Logic.CASTLE((PIECE_COLOR / 6), from_row, from_col, to_row, to_col)
            return Moves.KING_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
    
    @staticmethod
    def IS_SQUARE_ATTACKED(row, col, COLOR):
        for from_row in range(8):
            for from_col in range(8):
                piece = Board.LOGICAL_BOARD[from_row][from_col]
                if piece != 0 and (piece > 0) != (COLOR > 0):
                    if Logic.IS_VALID_MOVE(from_row, from_col, row, col) == True:
                        return True
        return False
    
    @staticmethod
    def IS_CHECK(COLOR):
        KING = 6 * COLOR
        for i in range(8):
            for j in range(8):
                if Board.LOGICAL_BOARD[i][j] == KING:
                    kings_row = i
                    kings_col = j

        return Logic.IS_SQUARE_ATTACKED(kings_row, kings_col, COLOR)

        

    # -------------------------------------
    #  DECLERATION FOR HANDLING CHECKMATE |
    # -------------------------------------

    @staticmethod
    def IS_CHECKMATE():
        ORIGINAL_TURN = Logic.TURN 
        for from_row in range(8):
            for from_col in range(8):
                piece = Board.LOGICAL_BOARD[from_row][from_col]
                if piece != 0 and (piece > 0) == (Logic.TURN > 0):
               
                    for to_row in range(8):
                        for to_col in range(8):
                            Logic.TURN = ORIGINAL_TURN
                            if Logic.IS_VALID_MOVE(from_row, from_col, to_row, to_col) == True:
                                saved_from = Board.LOGICAL_BOARD[from_row][from_col]
                                saved_to = Board.LOGICAL_BOARD[to_row][to_col]

                                Board.LOGICAL_BOARD[to_row][to_col] = saved_from
                                Board.LOGICAL_BOARD[from_row][from_col] = 0
                            
                                Logic.TURN = ORIGINAL_TURN
                                STILL_IN_CHECK = Logic.IS_CHECK(Logic.TURN)

                                Board.LOGICAL_BOARD[from_row][from_col] = saved_from
                                Board.LOGICAL_BOARD[to_row][to_col] = saved_to

                                Logic.TURN = ORIGINAL_TURN
                                if not STILL_IN_CHECK:
                                    return False

        return True
    

    # ----------------------------------------
    #  DECLERATION FOR KING CASTLE MOVEMENTS |
    # ----------------------------------------

    @staticmethod
    def CASTLE(KING_COLOR, from_row, from_col, to_row, to_col):

        if Board.BLACK_KING_MOVED and KING_COLOR < 0:
            return False
    
        if Board.WHITE_KING_MOVED and KING_COLOR > 0:
            return False


        IS_LEFT = False
        col_step = 1
        if(to_col < 4):
            IS_LEFT = True
            col_step *= -1

        #CHECK IS IN BOUNDS
        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False
    
        c = from_col + col_step
        #Check for pieces in the way
        while (from_row, c) != (from_row, to_col):
            if Board.LOGICAL_BOARD[from_row][c] != 0:
                return False  # something is in the way
            c += col_step
        
        #Check TO SEE IF ITS AN ENEMY ROOK
        target = Board.LOGICAL_BOARD[to_row][to_col]
        if target != 2 * KING_COLOR:
            return False
        
        step_col = from_col + col_step
        if Logic.IS_SQUARE_ATTACKED(from_row, from_col, KING_COLOR):
            return False
        if Logic.IS_SQUARE_ATTACKED(from_row, step_col, KING_COLOR):
            return False


        return True