from Board import Board
from Logic import Logic

class Opponent:
    PIECE_VALUES = {1: 100, 2: 500, 3: 320, 4: 330, 5: 900, 6: 20000}

    def GET_BOARD(piece, row, col):
        if piece == 1: 
            return Board.PAWN_TABLE[row][col]
        if piece == 2: 
            return Board.ROOK_TABLE[row][col]
        if piece == 3: 
            return Board.KNIGHT_TABLE[row][col]
        if piece == 4: 
            return Board.BISHOP_TABLE[row][col]
        if piece == 5: 
            return Board.QUEEN_TABLE[row][col]
        if piece == 6:
            return Board.KING_TABLE[row][col]
        
        return 0
    
    def GET_BOARD_EVALUATION():
        total = 0

        for row in range(8):
            for col in range(8):
                piece = Board.LOGICAL_BOARD[row][col]
                if piece == 0:
                    continue

                if piece > 0: #PIECE IS WHITE
                    value = Opponent.PIECE_VALUES[piece] +  Opponent.GET_BOARD(piece, 7 - row, col) #BOARD DEFAULT AS BLACK, TO READ FOR WHITE WE NEED TO READ BACKWARD 7 - row row IS (0-7) SO IT CANT RESULT IN A NEGATIVE
                else:
                    value = -1 * (Opponent.PIECE_VALUES[abs(piece)] +  Opponent.GET_BOARD(abs(piece), row, col))

                total += value
    
        return -1 * total
    
    @staticmethod
    def MINIMAX(depth, color, alpha, beta):
        MOVE_LIST = Logic.GENERATE_MOVES(color)

        if len(MOVE_LIST) == 0:
            if Logic.IS_CHECK(color):
                return (100000 + depth) * color #+depth SO SOONER MATES ARE PREFERED
            else:
                return 0
        if depth == 0:
            return Opponent.GET_BOARD_EVALUATION()
        
        if color == -1:
            best = -1000000 #LOW NUMBER SO THE FIRST POSSIBLE MOVE BECOMES THE NEW BEST
            
            for move in MOVE_LIST:
                record = Logic.MAKE_MOVE(*move)
                score = Opponent.MINIMAX(depth - 1, 1, alpha, beta)
                Logic.UNMAKE_MOVE(record)
                best = max(best, score)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best
        
        else:
            best = +1000000 #HIGH NUMBER SO THE FIRST POSSIBLE MOVE BECOMES THE NEW BEST
            for move in MOVE_LIST:
                record = Logic.MAKE_MOVE(*move)
                score = Opponent.MINIMAX(depth - 1, -1, alpha, beta)
                Logic.UNMAKE_MOVE(record)
                best = min(best, score) #MIN B/C OF HPW EVALUATION IS HANDLES + IS GOOD FO BLACK 
                beta = min(beta, best)

                if beta <= alpha:
                    break

            return best
        
    

    @staticmethod
    def MAKE_BEST_MOVE(depth):
        MOVE_LIST = Logic.GENERATE_MOVES(-1)

        alpha = -1000000
        beta = 1000000

        best = -1000000 #LOW NUMBER SO THE FIRST POSSIBLE MOVE BECOMES THE NEW BEST
        best_move = MOVE_LIST[0]
        for move in MOVE_LIST:
            record = Logic.MAKE_MOVE(*move)
            score = Opponent.MINIMAX(depth - 1, 1, alpha, beta)
            Logic.UNMAKE_MOVE(record)
            if score > best:
                best = score
                best_move = move
            alpha = max(alpha, best)

        return best_move