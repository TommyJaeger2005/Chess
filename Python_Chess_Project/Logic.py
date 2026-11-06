from Board import Board
from Assets import Assets
from UI import UI
from Moves import Moves

class Logic:

    SELECTED = None
    TURN = 1 # 1 for WHITE -1 for BLACK



    # ------------------------
    #  #LOGIC FOR USER MOVES |
    # ------------------------

    @staticmethod
    def ON_CLICK(event):

        if Logic.TURN == -1:
            return
        col = event.x // 100
        row = event.y // 100

        if Logic.SELECTED is None:
            piece = Board.LOGICAL_BOARD[row][col] #GET PIECE VALUE TO CHECK WHITE OR BLACK
            if Board.LOGICAL_BOARD[row][col] != 0 and (piece > 0) == (Logic.TURN > 0):
                Logic.SELECTED = (row, col)
        else:
            from_row, from_col = Logic.SELECTED
            piece = Board.LOGICAL_BOARD[from_row][from_col]

            TARGET = Board.LOGICAL_BOARD[row][col] #CHECK THE GOAL POSITION TO MOVE TOO

            IS_CASTLE = False

            if abs(piece) == 6 and abs(TARGET) == 2 and piece * TARGET > 0:
                IS_CASTLE = True

            if TARGET == 0 or (TARGET > 0) != (Logic.TURN > 0) or IS_CASTLE: #CHECKS IF SPACE IS EMPTY OR THE OCCUPYING PIECE IS OF DIFFRENT COLOR
                if Logic.IS_VALID_MOVE(from_row, from_col, row, col):
                    record = Logic.MAKE_MOVE(from_row, from_col, row, col)

                    if Logic.IS_CHECK(Logic.TURN): #START REVERT FOR MOVE ENDING IN CHECK
                        Logic.UNMAKE_MOVE(record)
                        Logic.SELECTED = (row, col)

                    else:
                        Logic.TURN *= -1 #SWITCHES TURNS
                        Logic.SELECTED = None
                        if record["piece"] == 1 and row == 0:
                            Assets.PAWN_PROMOTION(row, col)
                        
                        UI.REDRAW() #DRAW BEFORE ANY POPUPS OCCUR

                        no_legal_moves = Logic.IS_CHECKMATE()

                        if Logic.IS_CHECK(Logic.TURN):  # is the NEW player now in check?
                            if no_legal_moves:
                                print("CHECKMATE")
                                Assets.CHECKMATE_POPUP()
                        else:
                            if no_legal_moves: #If THERE IS NO PRIOR CHECK THEN ITS STALEMATE:
                                print("STALEMATE")
                                Assets.STALEMATE_POPUP()
                        
                        if not no_legal_moves:
                            UI.GAME_FRAME.after(50, Logic.AI_TURN) #AFTER CREATES A PAUSE SO THE USER POSITION DRAWS
            else:
                Logic.SELECTED = (row, col) #CASE WHERE SELECTION DOES NOT MEET CRITERA



    # ---------------
    #  #AI TURN     |
    # ---------------
    
    @staticmethod
    def AI_TURN():
        from Opponent import Opponent
        move = Opponent.MAKE_BEST_MOVE(3)
        Logic.MAKE_MOVE(*move)
        Logic.TURN *= -1

        UI.REDRAW() #DRAE BEFORE ANY POPUS CAN OCCUR

        no_legal_moves = Logic.IS_CHECKMATE()

        if Logic.IS_CHECK(Logic.TURN):  # is the NEW player now in check?
            if no_legal_moves:
                print("CHECKMATE")
                Assets.CHECKMATE_POPUP()

        else:
            if no_legal_moves: #If THERE IS NO PRIOR CHECK THEN ITS STALEMATE:
                print("STALEMATE")
                Assets.STALEMATE_POPUP()



    # ----------------------
    #  #LOGIC FOR AI MOVES |
    # ----------------------

    @staticmethod
    def GENERATE_MOVES(color):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = Board.LOGICAL_BOARD[row][col]

                if piece == 0:
                    continue

                if (piece > 0) != (color > 0):
                    continue

                for to_row in range(8):
                    for to_col in range(8):
                        TARGET = Board.LOGICAL_BOARD[to_row][to_col] #CHECK THE GOAL POSITION TO MOVE TOO

                        IS_CASTLE = False

                        if abs(piece) == 6 and abs(TARGET) == 2 and piece * TARGET > 0:
                            IS_CASTLE = True

                        if TARGET == 0 or (TARGET > 0) != (color > 0) or IS_CASTLE: #CHECKS IF SPACE IS EMPTY OR THE OCCUPYING PIECE IS OF DIFFRENT COLOR
                            if Logic.IS_VALID_MOVE(row, col, to_row, to_col):
                                record = Logic.MAKE_MOVE(row, col, to_row, to_col)
                                if Logic.IS_CHECK(color): 
                                    Logic.UNMAKE_MOVE(record)
                                else:
                                    moves.append((row, col, to_row, to_col))
                                    Logic.UNMAKE_MOVE(record)
        return moves



    # --------------------------
    #  #LOGIC FOR MAKING MOVES |
    # --------------------------

    @staticmethod
    def MAKE_MOVE(from_row, from_col, to_row, to_col):
        #ASSUME MOVE IS LEGAL
        piece = Board.LOGICAL_BOARD[from_row][from_col]   #GET THE PIECE
        TARGET = Board.LOGICAL_BOARD[to_row][to_col]      #WHAT IS ON THE DESTINATION

        record = {
            "from": (from_row, from_col),
            "to": (to_row, to_col),
            "piece": piece,
            "target": TARGET,
            "is_castle": False,
            "is_left": False,
            "is_ep": False,
            "ep_pawn": 0,
            "old_ep_flag": Board.IS_EN_PASSANT,
            "old_ep_row": Board.EN_PASSANT_ROW,
            "old_ep_col": Board.EN_PASSANT_COL,
            "old_white_king_moved": Board.WHITE_KING_MOVED,
            "old_black_king_moved": Board.BLACK_KING_MOVED,
        }

        record["old_white_left_rook_moved"] = Board.WHITE_LEFT_ROOK_MOVE
        record["old_white_right_rook_moved"] = Board.WHITE_RIGHT_ROOK_MOVE
        record["old_black_left_rook_moved"] = Board.BLACK_LEFT_ROOK_MOVE
        record["old_black_right_rook_moved"] = Board.BLACK_RIGHT_ROOK_MOVE

        #KING MOVING ONTO ITS OWN ROOK IS A CASTLE
        if abs(piece) == 6 and abs(TARGET) == 2 and piece * TARGET > 0:
            record["is_castle"] = True
            record["is_left"] = to_col < 4   #THE ROOK IS THE DESTINATION, SO to_col IS THE ROOK'S COLUMN

        #PAWN MOVING DIAGONALLY ONTO AN EMPTY SQUARE IS EN PASSANT
        if abs(piece) == 1 and TARGET == 0 and abs(from_col - to_col) == 1:
            record["is_ep"] = True
            record["ep_pawn"] = Board.LOGICAL_BOARD[from_row][to_col]

        if record["is_castle"]:
            #START CASTLE MOVE
            Board.LOGICAL_BOARD[from_row][from_col] = 0
            Board.LOGICAL_BOARD[to_row][to_col] = 0

            #MOVE THE PIECES
            if record["is_left"]:
                Board.LOGICAL_BOARD[to_row][from_col - 2] = piece
                Board.LOGICAL_BOARD[to_row][from_col - 1] = TARGET
            else:
                Board.LOGICAL_BOARD[to_row][from_col + 2] = piece
                Board.LOGICAL_BOARD[to_row][from_col + 1] = TARGET
            #END CASTLE MOVE

        else:
            #MAKE THE MOVE
            Board.LOGICAL_BOARD[to_row][to_col] = piece
            Board.LOGICAL_BOARD[from_row][from_col] = 0

            #REMOVE THE PAWN CAPTURED EN PASSANT
            if record["is_ep"]:
                Board.LOGICAL_BOARD[from_row][to_col] = 0

            #AUTO PROMOTE TO QUEEN (HUMAN POPUP HAPPENS LATER IN ON_CLICK)
            if abs(piece) == 1 and (to_row == 0 or to_row == 7):
                Board.LOGICAL_BOARD[to_row][to_col] = 5 * (1 if piece > 0 else -1)

        #UPDATE EN PASSANT FLAGS (RECORD ALREADY HOLDS THE OLD VALUES)
        if abs(piece) == 1 and abs(from_row - to_row) == 2:
            Board.IS_EN_PASSANT = True
            Board.EN_PASSANT_ROW = (from_row + to_row) // 2
            Board.EN_PASSANT_COL = to_col
        else:
            Board.IS_EN_PASSANT = False

        #UPDATE KING MOVED FLAGS (ALSO COVERS CASTLING)
        if abs(piece) == 6:
            if piece > 0:
                Board.WHITE_KING_MOVED = True
            else:
                Board.BLACK_KING_MOVED = True

        # UPDATE ROOK MOVED FLAGS
        if abs(piece) == 2:
            if from_row == 7 and from_col == 0:
                Board.WHITE_LEFT_ROOK_MOVE = True
            elif from_row == 7 and from_col == 7:
                Board.WHITE_RIGHT_ROOK_MOVE = True
        else:
            if from_row == 0 and from_col == 0:
                Board.BLACK_LEFT_ROOK_MOVE = True
            elif from_row == 0 and from_col == 7:
                Board.BLACK_RIGHT_ROOK_MOVE = True

        return record

    
    
    # ----------------------------
    #  #LOGIC FOR UNMAKING MOVES |
    # ----------------------------

    @staticmethod
    def UNMAKE_MOVE(record):
        from_row, from_col = record["from"]
        to_row, to_col = record["to"]
        piece = record["piece"]
        target = record["target"]

        #RESTORE THE FLAGS
        Board.IS_EN_PASSANT = record["old_ep_flag"]
        Board.EN_PASSANT_ROW = record["old_ep_row"]
        Board.EN_PASSANT_COL = record["old_ep_col"]
        Board.WHITE_KING_MOVED = record["old_white_king_moved"]
        Board.BLACK_KING_MOVED = record["old_black_king_moved"]
        Board.WHITE_LEFT_ROOK_MOVE = record["old_white_left_rook_moved"]
        Board.WHITE_RIGHT_ROOK_MOVE = record["old_white_right_rook_moved"]
        Board.BLACK_LEFT_ROOK_MOVE = record["old_black_left_rook_moved"]
        Board.BLACK_RIGHT_ROOK_MOVE = record["old_black_right_rook_moved"]

        if record["is_castle"]:
            #CLEAR THE NEW KING AND ROOK SQUARES FIRST
            if record["is_left"]:
                Board.LOGICAL_BOARD[to_row][from_col - 2] = 0
                Board.LOGICAL_BOARD[to_row][from_col - 1] = 0
            else:
                Board.LOGICAL_BOARD[to_row][from_col + 2] = 0
                Board.LOGICAL_BOARD[to_row][from_col + 1] = 0

            #THEN PUT THE KING AND ROOK BACK
            Board.LOGICAL_BOARD[from_row][from_col] = piece
            Board.LOGICAL_BOARD[to_row][to_col] = target

        else:
            #RESTORE THE ORIGINAL PIECE FROM THE RECORD (THIS ALSO UNDOES PROMOTION)
            Board.LOGICAL_BOARD[from_row][from_col] = piece
            Board.LOGICAL_BOARD[to_row][to_col] = target

            #PUT BACK THE PAWN CAPTURED EN PASSANT
            if record["is_ep"]:
                Board.LOGICAL_BOARD[from_row][to_col] = record["ep_pawn"]



    # ---------------------------------------------------------
    #  #CALLS THE MOVE VALIDATION BASED ON THE SELECTED PIECE |
    # ---------------------------------------------------------

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
            if(Board.LOGICAL_BOARD[to_row][to_col] == 2 * (PIECE_COLOR / 6)):
                return Logic.CASTLE((PIECE_COLOR / 6), from_row, from_col, to_row, to_col)
            return Moves.KING_MOVES(PIECE_COLOR, from_row, from_col, to_row, to_col)
    
    @staticmethod
    def IS_SQUARE_ATTACKED(row, col, COLOR):
        for from_row in range(8):
            for from_col in range(8):
                piece = Board.LOGICAL_BOARD[from_row][from_col]

                if piece != 0 and (piece > 0) != (COLOR > 0):

                    if abs(piece) == 1:
                        direction = -1 if piece > 0 else 1
                        if row == from_row + direction and abs(col - from_col) == 1:
                            return True
                    else:
                        if Logic.IS_VALID_MOVE(from_row, from_col, row, col):
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
        
        return False
        

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
        #HANDLES BLACK VALIDATION
        if Board.BLACK_KING_MOVED and KING_COLOR < 0:
            return False
        
        if Board.BLACK_LEFT_ROOK_MOVE and KING_COLOR < 0:
            return False
        
        if Board.BLACK_RIGHT_ROOK_MOVE and KING_COLOR < 0:
            return False
        
        #HANDLES WHITE VALIDATION
        if Board.WHITE_KING_MOVED and KING_COLOR > 0:
            return False
        
        if Board.WHITE_LEFT_ROOK_MOVE and KING_COLOR > 0:
            return False
        
        if Board.WHITE_RIGHT_ROOK_MOVE and KING_COLOR > 0:
            return False
        
        #START LOGIC
        IS_LEFT = False
        col_step = 1
        if to_col > from_col:
            col_step =1
        else:
            col_step = -1

        #CHECK IS IN BOUNDS
        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False
    
        c = from_col + col_step
        #Check for pieces in the way
        while (from_row, c) != (from_row, to_col):
            if not (0 <= c <= 7):
                return False
    
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