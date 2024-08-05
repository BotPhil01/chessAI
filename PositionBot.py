import chess
from RegularBot import calc_pos_adv, game_over_value

class PositionBot:
    def __str__(self):
        return "PositionBot"
    def eval_board(self, board: chess.Board):
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
        return calc_pos_adv(wp, bp, wr, br, wn, bn, wb, bb, wq, bq, wk, bk)