import chess
import chess.polyglot
import BoardEvaluation

depth = 10
board = chess.Board()
move_val = -9999
def set_board(_board):
    global board
    board = _board

def set_depth(_depth):
    global depth
    depth = _depth


def next_move(_board):
    set_board(_board)
    try:
        move = chess.polyglot.MemoryMappedReader(
            "resources/computer.bin").weighted_choice(
            board).move
        return move
    except:
        best_move = chess.Move.null()
        best_val = -99999
        alpha = -100000
        beta = 100000
        qlim = 64
        for move in board.legal_moves:
            board.push(move)
            move_value = -alphabeta(-beta, -alpha, depth - 1, qlim)
            if move_value > best_val:
                best_move = move
                best_val = move_value
            if move_value > alpha:
                alpha = move_value
            board.pop()
        return best_move


# alpha beta function for move generation
# alpha = lower bound
# beta = upper bound
def alphabeta(alpha, beta, _depth, qlim):
    best_val = -9999
    # if there are no more moves to play do quiescence search
    if (_depth == 0):
        return quiesce(alpha, beta, qlim)
    # else keep playing moves and evaluating
    for move in board.legal_moves:
        board.push(move)  # play move
        global move_val
        move_val = -alphabeta(-beta, -alpha, _depth - 1, qlim)  # do alpha beta on blacks move
        board.pop()  # remove move
        if move_val >= beta:
            return move_val
        if move_val > best_val:
            best_val = move_val
        if move_val > alpha:
            alpha = move_val
    return best_val

# search algorithm to evaluate quiet moves
def quiesce(alpha, beta, lim):
    evaluator = BoardEvaluation
    evaluator.set_board(board)
    eval = evaluator.evaluateboard()
    global move_val
    if eval >= beta:
        return beta
    if alpha < eval:
        alpha = eval
    for move in board.legal_moves:
        if board.is_capture(move) and lim > 0:
            board.push(move)
            lim -= 1
            move_val = -quiesce(-beta, -alpha, lim)
            board.pop()
    if move_val >= beta:
        return beta
    if move_val > alpha:
        alpha = move_val
    return alpha



