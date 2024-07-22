import chess
board = chess.Board()

def set_board(_board):
    global board
    board = _board
def getgameresult():
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return 9999
        else:
            return -9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0


#returns the current material advantage of the board
def calcmatadv():
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    wk = len(board.pieces(chess.KING, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    bk = len(board.pieces(chess.KING, chess.BLACK))
    material = 100 * (wp - bp) + 450 * (wr - br) + 300 * (wn - bn) + 330 * (wb - bb) + 900 * (wq - bq)
    return material


#Function to give the current position advantage
def calcposadv():
    pawnTable = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -20, -20, 10, 10, 5,
        5, -5, -10, 0, 0, -10, -5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
    knightTable = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ]
    bishopTable = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]
    rookTable = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
    queenTable = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 5, 5, 5, 5, 5, 0, -10,
        0, 0, 5, 5, 5, 5, 0, -5,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]
    kingTable = [
        20, 30, 10, 0, 0, 10, 30, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]

    pawns = sum(pawnTable[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawns += sum(-pawnTable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))

    rooks = sum(rookTable[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    rooks += sum(-rookTable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))

    knights = sum(knightTable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    knights += sum(-knightTable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))

    bishops = sum(bishopTable[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishops += sum(-bishopTable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))

    queens = sum(queenTable[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    queens += sum(-queenTable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))

    kings = sum(kingTable[i] for i in board.pieces(chess.KING, chess.WHITE))
    kings += sum(-kingTable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK))
    return sum([pawns, rooks, knights, bishops, queens, kings])


def evaluateboard():
    if board.is_game_over():
        return getgameresult()
    advantage = calcposadv() + calcmatadv()
    if board.turn:
        return advantage
    return -advantage

