import utils
from constants import N, W, A

def refine(board, pos, fpositions, chain = []):
    """ 
    Returns the refined future positions for given stone,
    by applying game constraints.
    Also appends the move type to each possible position.
    Essentially this is the game's logic.
        the f in fpos, fpositions stands for "future".
    """
    refined = []
    for fpos in fpositions:
        x, y = fpos # future position
        ox, oy = pos # old position
        d = utils.tsub(fpos, pos) #direction
        
        # check for validity when chaining:
        #    - have we already visited the future position?
        #    - is the direction the same as before?
        # for more info on this look up the fanorona rules.
        if chain:
            if fpos in chain or d == utils.tsub(pos, chain[-2]):
                continue
            
        # approach
        ax, ay = utils.tadd(fpos, d)
        if board.valid((ax, ay)) and not board.empty((ax, ay)) and board[ax][ay] != board[ox][oy]:
            refined.append((x, y, A))
        
        # withdraw
        wx, wy = utils.tsub(pos, d)
        if board.valid((wx, wy)) and not board.empty((wx, wy)) and board[wx][wy] != board[ox][oy]:
            refined.append((x, y, W))
    
    # if no capturing moves found and not chaining, use paikas.
    if not refined and not chain:
        for fpos in fpositions:
            x, y = fpos
            refined.append((x, y, N))
        
    return refined