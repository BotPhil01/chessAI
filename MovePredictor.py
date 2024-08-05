import chess
from chess.polyglot import MemoryMappedReader
from RegularBot import RegularBot
# alpha = min assured score (board after best opponent move)
# beta = max assured score (board after best pov player move)
# when beta < alpha prune branch
MAX_DEPTH = 5
MAX_QUIESCE_DEPTH = 2

def set_depth(depth):
    global MAX_DEPTH
    MAX_DEPTH = depth



def alpha_beta(board, whi, dep, alp, bet, engine):
    if dep == MAX_DEPTH:
        return quiesce(board, alp, bet, engine, 0)
    best = float("-inf")
    for move in board.legal_moves:
        board.push(move)
        score = -alpha_beta(board, not whi, dep + 1, -alp, -bet, engine)
        board.pop()
        if score > best:
            best = score
            if score > alp:
                alp = score
        if score >= bet:
            return best
    return best

def quiesce(board: chess.Board, alpha, beta, engine: RegularBot, qdepth): # searches the captures remaining
    stand_pat = engine.eval_board(board)
    if qdepth == MAX_QUIESCE_DEPTH:
        return stand_pat
    if stand_pat >= beta:
        return beta
    if stand_pat < alpha:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(board, -beta, -alpha, engine, qdepth + 1)
            board.pop()

            if score >= beta:
                return beta
            if score < alpha:
                alpha = score
    return alpha


def next_move(board, engine):
    if board.is_game_over():
        raise Exception("Game has already finished")
    else:
        try:
            return MemoryMappedReader("resources/Chess-World-master/books/human.bin").weighted_choice(board).move
        except IndexError:
            best_move = None
            best_eval = float("-inf")
            alpha = float("-inf")
            beta = float("inf")
            for move in board.legal_moves:
                if move != None:
                    board.push(move)
                    tmp = -alpha_beta(board, board.turn == chess.WHITE, 0, -alpha, -beta, engine)
                    board.pop()
                    if tmp > best_eval:
                        best_eval = tmp
                        best_move = move
                    if tmp > alpha:
                        alpha = tmp
            if best_move == None:
                raise Exception("No valid move")
            return best_move
