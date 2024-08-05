import chess
board = None
# tables
# unreachables are 0
# want inital postiion to be negative / low positive
# bad positions are negative
# good positions are positive
class Evaluator:
    PAWN_TABLE = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 5, 10, -20, -20, 10, 5, 5,
        10, 15, 25, -10, -10, 5, 15, 10,
        10, 0, 25, 40, 40, 25, 0, 10,
        0, 0, 25, 45, 45, 25, 0, 0,
        5, 5, 30, 50, 50, 30, 5, 5,
        10, 10, 10, 60, 60, 60, 10, 10,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    ROOK_TABLE = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    KNIGHT_TABLE = [
        -10, -5, -5, -5, -5, -5, -5, -10,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 40, 30, 30, 40, 0, -5,
        -5, 35, 35, 50, 50, 35, 35, -5,
        -5, 25, 25, 50, 50, 25, 25, -5,
        -5, 25, 25, 25, 25, 25, 25, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -10, -5, -5, -5, -5, -5, -5, -10
    ]

    BISHOP_TABLE = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 10, 0, 0, 0, 0, 10, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]

    QUEEN_TABLE = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 5, 5, 5, 5, 5, 0, -10,
        0, 0, 5, 10, 10, 5, 0, -5,
        -5, 0, 5, 10, 10, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]

    KING_TABLE = [
        20, 30, 10, 0, 0, 10, 30, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]


    def __init__(self):
        self.board = chess.Board()

    def set_board(self, b):
        global board
        board = b

    def eval_board(self):
        # game ended
        global board
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return 9999
            return -9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        # board evaluation if not ended
        wp = board.pieces(chess.PAWN, chess.WHITE)
        bp = board.pieces(chess.PAWN, chess.BLACK)
        wr = board.pieces(chess.ROOK, chess.WHITE)
        br = board.pieces(chess.ROOK, chess.BLACK)
        wn = board.pieces(chess.KNIGHT, chess.WHITE)
        bn = board.pieces(chess.KNIGHT, chess.BLACK)
        wb = board.pieces(chess.BISHOP, chess.WHITE)
        bb = board.pieces(chess.BISHOP, chess.BLACK)
        wq = board.pieces(chess.QUEEN, chess.WHITE)
        bq = board.pieces(chess.QUEEN, chess.BLACK)
        wk = board.pieces(chess.KING, chess.WHITE)
        bk = board.pieces(chess.KING, chess.BLACK)
        # calculate material advantage and positional advantage
        mat_adv = self.calc_mat_adv(len(wp), len(bp), len(wr), len(br), len(wn), len(bn), len(wb), len(bb), len(wq), len(bq))
        pos_adv = self.calc_pos_adv(wp, bp, wr, br, wn, bn, wb, bb, wq, bq, wk, bk)
        return  mat_adv + pos_adv

    def calc_mat_adv(self, wp: int, bp: int, wr: int, br: int, wn: int, bn:int, wb: int, bb: int, wq: int, bq: int): # returns material adv
        return wp - bp + 5 * (wr - br) + 3 * (wb + wn - bb - bn) + 7 * (wq - bq)

    def calc_pos_adv(self, wp, bp, wr, br, wn, bn, wb, bb, wq, bq, wk, bk): # returns positional advantage
        ret = sum(self.PAWN_TABLE[i] for i in wp)
        ret += sum(-self.PAWN_TABLE[chess.square_mirror(i)] for i in bp)
        ret += sum(self.ROOK_TABLE[i] for i in wr)
        ret += sum(-self.ROOK_TABLE[chess.square_mirror(i)] for i in br)
        ret += sum(self.BISHOP_TABLE[i] for i in wb)
        ret += sum(-self.BISHOP_TABLE[chess.square_mirror(i)] for i in bb)
        ret += sum(self.KNIGHT_TABLE[i] for i in wn)
        ret += sum(-self.KNIGHT_TABLE[chess.square_mirror(i)] for i in bn)
        ret += sum(self.QUEEN_TABLE[i] for i in wq)
        ret += sum(-self.QUEEN_TABLE[chess.square_mirror(i)] for i in bq)
        ret += sum(self.KING_TABLE[i] for i in wk)
        ret += sum(-self.KING_TABLE[chess.square_mirror(i)] for i in bk)
        return ret