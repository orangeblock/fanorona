import game
def ab_pruning(state, depth):
    v = max_value(state, -1000, 1000, depth)
    #print v
    for child in state.blackChildren:
        if child[0].score == v:
            return child

def max_value(state, a, b, depth):
    if depth == 0 or state.cpuWins() or state.isTerminal():
        state.score = state.eval(game.cpu)
        return state.score

    v = -1000
    children = state.getChildren(game.cpu)
    for child in children:
        v = max(v, min_value(child[0], a, b, depth-1))
        if v >= b:
            state.score = v
            return v
        a = max(a, v)
    state.score = v
    return v

def min_value(state, a, b, depth):
    if depth == 0 or state.playerWins() or state.isTerminal():
        state.score = state.eval(game.player)
        return state.score

    v = 1000
    children = state.getChildren(game.player)
    for child in children:
        v = min(v, max_value(child[0], a, b, depth-1))
        if v <= a:
            state.score = v
            return v
        b = min(b, v)
    state.score = v
    return v