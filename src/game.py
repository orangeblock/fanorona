from board import Board
import logic
import gfxgrid
import gfxglow
import gfxring
import ai
from constants import *
import pygame
import itertools

cpu = BLACK
player = WHITE
current = player
winner = None

# Game States
# -----------
# game over
finished = False
# player is selecting a move (out of possible ones)
choice = False
# a stone is graphically moving
moving = False
# player resolves ambiguous moves (have both withdrawal and approach captures)
resolving = False
# player continues to chain captures.
chaining = False
# -----------

board = None
grid = None
rgroup = None
ggroup = None
clock = None
def init():
    global rgroup, ggroup, clock, board, grid, current
    board = Board()
    board.children = ai.successors(board, current)
    grid = gfxgrid.Grid(board)
    rgroup = pygame.sprite.Group()
    ggroup = pygame.sprite.Group()
    clock = pygame.time.Clock()

chains = []
captured = []
lastpos = None
def player_move(sel):
    global moving, chains, captured, lastpos, board, choice, grid, resolving, chaining
    if moving: return
    if resolving and sel in itertools.chain.from_iterable([c[0] for c in captured]):
        # resolved
        for cap in captured:
            if sel in cap[0]:
                resolving = False
                for i, chain in enumerate(chains):
                    if chain[0] != cap[1]:
                        del chains[i]
                break
        captured = []
        move()
        return
    if choice:
        if sel in [chain[0][0] for chain in chains]:
            # choosing where to advance
            choice = False
            rgroup.empty()
            ggroup.empty()
            grid.move(lastpos, sel)
            chains = [c for c in chains if c[0][0] == sel]
            # find if move is ambiguous
            first = [c[0] for c in chains]
            if any(tup[1] == A for tup in first) and any(tup[1] == W for tup in first):
                captured.append((logic.captured(board, lastpos, (sel, A)),(sel,A)))
                captured.append((logic.captured(board, lastpos, (sel, W)),(sel,W)))
            return
        elif not chaining:
            lastpos = None
            choice = False
    if not lastpos and sel and sel in board.colored(player):
        # first selection
        chains = [x[2] for x in board.children if x[1] == sel]
        add_ring([sel])
        add_glow(set([chain[0][0] for chain in chains]))
        if chains:
            choice = True
            lastpos = sel
        return
        
def move():
    global captured, chains, lastpos, resolving, board, choice, grid, chaining
    if captured:
        # ambiguity needs to be resolved first
        add_ring(itertools.chain.from_iterable([c[0] for c in captured]))
        resolving = True
    else:
        # make the move on the board and remove captured pieces
        cap = logic.captured(board, lastpos, chains[0][0])
        board.remove(cap)
        grid.remove(cap)
        board.move(lastpos, chains[0][0][0])
        lastpos = chains[0][0][0]
        # advance in the chains
        for i in range(len(chains)):
            del chains[i][0]
            
        newchains = []
        for chain in chains:
            if chain:
                newchains.append(chain)
        chains = newchains
        
        if chains:
            # continue chaining
            chaining = True
            add_ring([lastpos])
            add_glow(set([chain[0][0] for chain in chains]))
            choice = True
        else:
            end_turn()
            
def end_turn():
    global current, lastpos, ggroup, rgroup, chaining
    ggroup.empty()
    rgroup.empty()
    current = cpu
    lastpos = None
    chaining = False
    board.children = []

def add_ring(positions):
    global rgroup
    rgroup.empty()
    for x,y in positions:
        rgroup.add(gfxring.Ring(grid[x][y].rect))
        
def add_glow(positions):
    global ggroup
    ggroup.empty()
    for x,y in positions:
        ggroup.add(gfxglow.Glow(grid[x][y].rect))

def game_over():
    global winner
    if board.terminal():
        if len(board.colored(cpu)) > 0:
            winner = cpu
        else:
            winner = player
        return True
    return False

### CPU BELOW
decision = None
last = None
first = True
cpucaptured = []
def cpu_move():
    global board, decision, last, first, current, moving, cpucaptured
    if moving: return
    if first:
        first = False
        decision = ai.decide(board, cpu)
        cpucaptured = logic.captured(board, decision[1], decision[2][0])
        board.remove(cpucaptured)
        board.move(decision[1], decision[2][0][0])
        last = decision[2][0][0]
        grid.move(decision[1], decision[2][0][0])
        moving = True
    else:
        grid.remove(cpucaptured)
        chain = decision[2]
        del chain[0]
        if chain:
            cpucaptured = logic.captured(board, last, chain[0])
            board.remove(cpucaptured)
            board.move(last, chain[0][0])
            grid.move(last, chain[0][0])
            last = chain[0][0]
            moving = True
        else:
            first = True
            current = player
            board.children = ai.successors(board, player)