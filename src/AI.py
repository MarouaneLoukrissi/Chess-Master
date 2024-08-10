def minimax(state, depth, isMaxPlayer, alpha=float("-inf"), beta=float("inf"), transposition_table={}):
    if depth == 0:
        return state.eval(), state
    if isMaxPlayer:
        maxEval = float('-inf')
        bestMove = None
        for board in state.get_boards("white"):
            evaluation = minimax(board, depth - 1, False, alpha, beta, transposition_table)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                bestMove = board
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, bestMove
    else:
        miniEval = float('inf')
        bestMove = None
        for board in state.get_boards("black"):
            evaluation = minimax(board, depth - 1, True, alpha, beta, transposition_table)[0]
            miniEval = min(miniEval, evaluation)
            if miniEval == evaluation:
                bestMove = board
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return miniEval, bestMove
