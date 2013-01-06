import logic
import game
from constants import P

def decide(board, color):
    """ Decides and returns next move based on current board. """
    board.children = successors(board, color)
    decision = ab_prune(board, 1)
    board.children = []
    return decision

def successors(board, color):
    if board.children:
        return board.children
    stack = []
    children = []
    for pos in board.colored(color):
        if pos not in board.moves:
            continue
        start = pos
        chain = []
        tuples = []
        b = board.copy()
        
        tuples = board.moves[pos]
        while tuples:
            for move in tuples:
                cb = b.copy()
                newpos = move[0]
                cb.remove(logic.captured(cb, pos, move))
                cb.move(pos, newpos)
                if move[1] != P:
                    tups = logic.refine(cb, newpos, cb.adjacent(newpos), [((start), 0)] + chain)
                else:
                    tups = []
                chain.append(move)
                stack.append((cb.copy(), newpos, chain[:], tups[:]))
                del chain[-1]
            b, pos, chain, tuples = stack[-1]
            del stack[-1]
            while not tuples:
                children.append((b, start, chain))
                try:
                    b, pos, chain, tuples = stack[-1]
                    del stack[-1]
                except IndexError:
                    break
    return children

def evaluate(board, color):
    """
    Scores given board for given color.
    CPU is MAX, player is MIN. 
    """
    if color == game.player:
        return 22 - len(board.colored(color))
    else:
        return len(board.colored(color))

def ab_prune(board, depth):
    def max_value(state, a, b, depth, first = False):
        if not depth or state.terminal():
            state.score = evaluate(state, game.cpu)
            return state.score
    
        v = -1000
        children = successors(state, game.cpu)
        for child in children:
            v = max(v, min_value(child[0], a, b, depth-1))
            if v >= b:
                state.score = v
                return v
            a = max(a, v)
        state.score = v
        return v
    
    def min_value(state, a, b, depth):
        if not depth or state.terminal():
            state.score = evaluate(state, game.player)
            return state.score
    
        v = 1000
        children = successors(state, game.player)
        for child in children:
            v = min(v, max_value(child[0], a, b, depth-1))
            if v <= a:
                state.score = v
                return v
            b = min(b, v)
        state.score = v
        return v
    
    v = max_value(board, -1000, 1000, depth)
    for child in successors(board, game.cpu):
        if child[0].score == v:
            return child