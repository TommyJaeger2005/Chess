class Board:
    WHITE_KING_MOVED = False
    BLACK_KING_MOVED = False
    EN_PASSANT_ROW = 1000
    EN_PASSANT_COL = 1000
    IS_EN_PASSANT = False
    
    # ------------------------------------
    # LOGICAL BOARD AND PIECE MEANINGS!! |
    # ------------------------------------
    # POSTIVE VALUES = WHITE PIECES      |
    # NEGITIVE VALUES = BLACK PIECES     |
    # |1| = PAWN                         |
    # |2| = ROOK                         |
    # |3| = KNIGHT                       |
    # |4| = BISHOP                       |
    # |5| = QUEEN                        |
    # |6| = KING                         |
    # ------------------------------------

    LOGICAL_BOARD = [   
        [-2,-3,-4,-5,-6,-4,-3,-2],
        [-1,-1,-1,-1,-1,-1,-1,-1],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 1, 1, 1, 1, 1, 1, 1, 1],
        [ 2, 3, 4, 5, 6, 4, 3, 2],
    ]