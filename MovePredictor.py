import chess
from chess.polyglot import MemoryMappedReader
from Evaluation import Evaluator

# alpha = min assured score (board after best opponent move)
# beta = max assured score (board after best pov player move)
# when beta < alpha prune branch
MAX_DEPTH = 3


def set_depth(depth):
    global MAX_DEPTH
    MAX_DEPTH = depth


def alpha_beta(board: chess.Board, whi, dep, alp, bet): # white is maximising
    if dep == MAX_DEPTH:
        e = Evaluator()
        e.set_board(board)
        return quiesce(board, alp, bet)
    elif whi: # maximiser
        best = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            best = max(alpha_beta(board, False, dep + 1, alp, bet), best)
            alp = max(alp, best)
            board.pop()
            if bet <= alp:
                break
        return best
    else: # minimiser
        best = float("inf")
        for move in board.legal_moves:
            board.push(move)
            best = min(alpha_beta(board, True, dep + 1, bet, alp), best)
            bet = min(bet, best)
            board.pop()
            if bet <= alp:
                break
        return best


def quiesce(board: chess.Board, alpha, beta): # searches the captures remaining
    print("Quiescing")
    e = Evaluator()
    e.set_board(board)
    stand_pat = e.eval_board()
    if stand_pat >= beta:
        return beta
    if stand_pat < alpha:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score < alpha:
                alpha = score
    return alpha


def next_move(board):
    print("Getting next move")
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
                    tmp = -alpha_beta(board, board.turn == chess.WHITE, 0, alpha, beta)
                    board.pop()
                    if tmp > best_eval:
                        best_eval = tmp
                        best_move = move
                    if tmp > alpha:
                        alpha = tmp
            print("Found move")
            if best_move == None:
                raise Exception("No valid move")
            return best_move
