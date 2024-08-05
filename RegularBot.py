import chess

# tables
# unreachables are 0
# want inital postiion to be negative / low positive
# bad positions are negative
# good positions are positive

PAWN_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
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
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
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
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
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
Tables = [
    PAWN_TABLE, ROOK_TABLE, BISHOP_TABLE, KNIGHT_TABLE, QUEEN_TABLE, KING_TABLE
]


def calc_pos_adv(wp, bp, wr, br, wn, bn, wb, bb, wq, bq, wk, bk):  # returns positional advantage
    ret = 0
    ret += sum(PAWN_TABLE[i] for i in wp)
    ret += sum(-PAWN_TABLE[chess.square_mirror(i)] for i in bp)
    ret += sum(ROOK_TABLE[i] for i in wr)
    ret += sum(-ROOK_TABLE[chess.square_mirror(i)] for i in br)
    ret += sum(BISHOP_TABLE[i] for i in wb)
    ret += sum(-BISHOP_TABLE[chess.square_mirror(i)] for i in bb)
    ret += sum(KNIGHT_TABLE[i] for i in wn)
    ret += sum(-KNIGHT_TABLE[chess.square_mirror(i)] for i in bn)
    ret += sum(QUEEN_TABLE[i] for i in wq)
    ret += sum(-QUEEN_TABLE[chess.square_mirror(i)] for i in bq)
    ret += sum(KING_TABLE[i] for i in wk)
    ret += sum(-KING_TABLE[chess.square_mirror(i)] for i in bk)
    return ret


def calc_mat_adv(wp: int, bp: int, wr: int, br: int, wn: int, bn: int, wb: int, bb: int, wq: int,
                 bq: int):  # returns material adv
    return wp - bp + 5 * (wr - br) + 3 * (wb + wn - bb - bn) + 7 * (wq - bq)


def game_over_value(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return 9999
        return -9999
    return 0


class RegularBot:
    def __str__(self):
        return "RegularBot"

    def eval_board(self, board):
        # game ended
        if board.is_game_over(): return game_over_value(board)
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
        mat_adv = calc_mat_adv(len(wp), len(bp), len(wr), len(br), len(wn), len(bn), len(wb), len(bb), len(wq),
                               len(bq))
        pos_adv = calc_pos_adv(wp, bp, wr, br, wn, bn, wb, bb, wq, bq, wk, bk)
        return mat_adv + pos_adv
