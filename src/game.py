import pygame
from board import Board
import itertools
import gfxring, gfxtile, gfxglow, gfx
import minimax

BLACK = 0
WHITE = 1
current = WHITE


# Game States
# -----------
# game over
finished = False
# player is selecting a move (out of possible ones)
sel_move = False
# a stone is graphically moving
moving = False
# player resolves ambiguous moves (have both withdrawal and approach captures)
resolving = False
# player continues to chain captures.
chaining = False
# -----------

# color for each player
player = WHITE
cpu = BLACK

# fps clock
clock = None

# logical representation of board
board = None

# graphical representation of board
grid = None

# a container for the tile sprites
sgroup = None

# container for the ring decorator
rgroup = None

# a container for the glow animations
ggroup = None

# a dict of possible moves - dest : direction
pmoves = {}

# currently selected square by the player
cselected = None

# ambiguous captures 
acaptures1 = []
acaptures2 = []

lastPosition = None
lastDirection = None
path = []

def init():
    global rgroup, ggroup, clock, board
    board = Board()
    init_grid()
    rgroup = pygame.sprite.Group()
    ggroup = pygame.sprite.Group()
    clock = pygame.time.Clock()
              
# Graphically defines the 5x9 grid as a list of lists of Squares.
# Also creates a sprite group for easier redrawing.
def init_grid():
    global grid, sgroup
    grid = [[], [], [], [], []]
    sgroup = pygame.sprite.Group()
    xstart = 90
    ystart = 50
    for i in range(5):
        for j in range(9):
            xadd = j*60
            yadd = i*60
            grid[i].append(gfxtile.Square(i, j, pygame.Rect( (xstart + xadd, ystart + yadd), (60, 60) ), board[i][j]))
            sgroup.add(grid[i][j])

def player_move(mousepos):
    global cselected, sel_move, resolving, moving, capturing, chaining
    if moving: return
        
    for i in range(5):
        for j in range(9):
            if grid[i][j].rect.collidepoint(mousepos):
                sq = grid[i][j]
                if resolving:
                    if sq in acaptures1:
                        capture(0,0,0)
                    elif sq in acaptures2:
                        capture(0,0,1)
                elif chaining:
                    if sel_move and sq in pmoves:
                        rgroup.empty()
                        ggroup.empty()
                        gfx.move(cselected, sq, pmoves[sq])
                        sel_move = False
                        chaining = False
                        moving = True
                elif sel_move and sq in pmoves:
                    # move selected - stage of graphically moving it
                    rgroup.empty()
                    ggroup.empty()
                    gfx.move(cselected, sq, pmoves[sq])
                    sel_move = False
                    moving = True
                elif sq.stone and sq.stone.color == player:
                    # stage of selecting a stone
                    moves = board.getPossibleMoves(i, j, player)
                    set_glow(sq, moves)
                    set_ring([sq])
                    cselected = sq
                    sel_move = True
   
# sq - old square
# direction - the direction it has to follow to new square                 
def move(sq, direction):
    global lol
    if lol:
        return
    global lastDirection, lastPosition
    board[sq.x+direction[0]][sq.y+direction[1]] = board[sq.x][sq.y]
    board[sq.x][sq.y] = None
    path.append((sq.x, sq.y))
    lastDirection = direction
    lastPosition = add_tuple_elements((sq.x, sq.y), direction)
    capture(sq, direction)
               
# captures or does nothing if there is no capture.
# in case of ambiguity sets appropriate state & fields and returns.
# when the ambiguity is resolved it is called with a select argument.
def capture(start, direction, select = None):
    global acaptures1, acaptures2, current, cpu, resolving, rgroup
    
    if select is not None:
        #resolved ambiguity
        resolving = False
        rgroup.empty()
        if(select == 0):
            remove_stones(get_board_pos(acaptures1))
        elif(select == 1):
            remove_stones(get_board_pos(acaptures2))
        chain()
        return
        
    captured = board.getCaptured(start.x, start.y, current, direction)
    if len(captured[0]) > 0 and len(captured[1]) > 0:
        # ambiguity
        resolving = True
        acaptures1 = get_grid_squares(captured[0])
        acaptures2 = get_grid_squares(captured[1])
        set_ring(acaptures1+acaptures2)
        return
    
    # normal captures or no capture
    if len(captured[0]) > 0:
        remove_stones(captured[0])
        chain()
    elif len(captured[1]) > 0:
        remove_stones(captured[1])
        chain()
    else:
        current = cpu
        path = []
        chaining = False

def chain():
    global current, chaining, sel_move, lastPosition, lastDirection, cselected, path
    moves = board.getPossibleMoves(lastPosition[0], lastPosition[1], current, lastDirection, path)
    if len(moves) > 0:
        # chain    
        chaining = True    
        set_glow(grid[lastPosition[0]][lastPosition[1]], moves)
        set_ring([grid[lastPosition[0]][lastPosition[1]]])
        cselected = grid[lastPosition[0]][lastPosition[1]]
        sel_move = True
    else:
        current = cpu
        path = []
        chaining = False
            
# returns the grid squares of given board positions
# bpos is a list of tuples
def get_grid_squares(bpos):
    gsquares = []
    for pos in bpos:
        gsquares.append(grid[pos[0]][pos[1]])
    return gsquares

# opposite of the above
def get_board_pos(gpos):
    bpos = []
    for g in gpos:
        bpos.append((g.x, g.y))
    return bpos

def remove_stones(l):
    # remove the captured stones from the board
    board.remove(l)
    # and from the grid
    for s in l:
        grid[s[0]][s[1]].clearStone()
        
def set_ring(squares):
    rgroup.empty()
    for sq in squares:
        rgroup.add(gfxring.Ring(sq.rect))
    
def set_glow(sq, moves):
    global pmoves
    ggroup.empty()
    pmoves = {}
    if len(moves) > 0:
        for m in set(moves):
            ggroup.add(gfxglow.Glow( grid[sq.x+m[0]][sq.y+m[1]].rect ))
            pmoves[grid[sq.x+m[0]][sq.y+m[1]]] = iaxes(m)

def add_tuple_elements(tup1, tup2):
    return tuple(x + y for x,y in itertools.izip(tup1,tup2))

def iaxes(grid_pos):
    """
    Converts grid directions to screen directions.
    Grid directions have inverted x and y axes:
        x - rows (vertical)
        y - columns (horizontal)
    This needs to be inverted to represent directions on the screen.
    """
    return (grid_pos[1], grid_pos[0])

def game_over():
    if board.whiteCount == 0 or board.blackCount == 0:
        return True
    else:
        return False
    
# makes the move on the board and returns
# needed stuff for moving it graphically: (start/end squares and direction)
lol = False
def cpu_movee():
    global current, path
    children = board.getChildren(BLACK)
    print len(children)
    for child in children:
        print child[1]
        child[0].display()
        print child[0].eval(BLACK)
        print '--------------------------'
    current = player
    path = []
def cpu_move():
    global moving, current, lol, path # lol @ game.move
    lol = True
    if moving: return
    move = get_next_cpu_move()
    if move:
        sq = grid[move[0][0]][move[0][1]]
        sqn = grid[move[0][0]+move[1][0]][move[0][1]+move[1][1]]
        d = move[1]
        gfx.move(sq, sqn, iaxes(d))
        moving = True
    else:
        current = player
        path = []
        lol = False
        
cpu_index = None
cpu_moves = None
curr = None
def cpu_select():
    global cpu_moves, cpu_index, board
    if len(board.getChildren(BLACK)) == 0:
        board.display()
    choice = minimax.ab_pruning(board, 1)
    print choice
    cpu_moves = choice[1]
    cpu_index = 0
    return cpu_moves[0]

def get_next_cpu_move():
    global cpu_index, cpu_moves, board
    if cpu_index == None:
        return cpu_select()
    else:
        move = cpu_moves[cpu_index]
        sq = grid[move[0][0]][move[0][1]]
        d = move[1]
        a, w = board.getCaptured(sq.x, sq.y, current, d)
        board.move(sq.x, sq.y, d)
        if len(a) > 0 and len(w) > 0:
            if move[2] == 0:
                remove_stones(a)
            elif move[2] == 1:
                remove_stones(w)
        else:
            remove_stones(a+w)
            
        cpu_index+=1
        if cpu_index == len(cpu_moves):
            cpu_index = None
            cpu_moves = None
            return []
        else:
            return cpu_moves[cpu_index]