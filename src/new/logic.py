import utils
from constants import P, A, W

def refine(board, pos, fpositions, chain = []):
    """ 
    Returns the refined future positions for given stone,
    by applying game constraints.
    Also appends the move type to each possible position.
    
    *The f in fpos, fpositions stands for "future".
    """
    if chain:
        chain = [v[0] for v in chain]
    refined = []
    for fpos in fpositions:
        x, y = pos # old position
        d = utils.tsub(fpos, pos) #direction
        
        # check for validity when chaining:
        #    - have we already visited the future position?
        #    - is the direction the same as before?
        # for more info on this look up the fanorona rules.
        if chain:
            if fpos in chain or d == utils.tsub(pos, chain[-1]):
                continue
            
        # approach
        ax, ay = utils.tadd(fpos, d)
        if board.valid((ax, ay)) and not board.empty((ax, ay)) and board[ax][ay] != board[x][y]:
            refined.append((fpos, A))
        
        # withdraw
        wx, wy = utils.tsub(pos, d)
        if board.valid((wx, wy)) and not board.empty((wx, wy)) and board[wx][wy] != board[x][y]:
            refined.append((fpos, W))
    
    # if no capturing moves found and not chaining, return paikas.
    if not refined and not chain:
        for fpos in fpositions:
            refined.append((fpos, P))
        
    return refined

def clean(moves):
    """
    Removes positions that don't have moves and
    cleans up unwanted paika moves (when capturing ones exist).
    """
    for k in list(moves):
        if not moves[k]:
            del moves[k]

    types = [move[1] for l in moves.itervalues() for move in l]
    if A in types or W in types:
        for k, v in moves.items():
            if P in [move[1] for move in v]:
                del moves[k]

def captured(board, pos, move):
    """ Returns a list of captured stones according to the capture type."""
    fpos, captype = move
    if captype == P:
        return []
    
    captured = []
    ox, oy = capx, capy = pos
    color = board[ox][oy]
    d = utils.tsub(fpos, pos)
    
    if captype == A:
        cpos = capx, capy = utils.tadd(fpos, d)
    else:
        cpos = capx, capy = utils.tsub(pos, d)
        
    while board.valid((capx, capy)) and not board.empty((capx, capy)) and board[capx][capy] != color:
        captured.append(cpos)
        if captype == A:
            cpos = capx, capy = utils.tadd(cpos, d)
        else:
            cpos = capx, capy = utils.tsub(cpos, d)
    return captured