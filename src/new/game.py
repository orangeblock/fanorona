from board import Board
import logic
import gfxgrid
import gfxglow
import gfxring
import ai
from constants import *
import gfx
import pygame

cpu = BLACK
player = WHITE
current = player

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

# flag for triggering logical move
moveit = False

board = None
grid = None
rgroup = None
ggroup = None
clock = None
startsel = None
lastsel = None # player's last selection
lastdest = None
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
stage = 0
prevs = ()
def player_move(mousepos):
    global chains, stage, grid, board, player, prevs
    global rgroup, ggroup
    if moving: return
    if stage == 3:
        capture()
        return
    s = grid.collision(mousepos)
    if s:
        if stage == 0:
            start(s)
            prevs = s
        elif stage == 1:
            select(s)
            prevs = s 
        elif stage == 2:
            resolve(s)

# stage 0       
def start(s):
    global chains, stage, grid, board
    rgroup.empty()
    ggroup.empty()
    chains = [x[2] for x in board.children if x[1] == s]
    rgroup.add(gfxring.Ring(grid[s[0]][s[1]].rect))
    if chains:
        for chain in chains:
            i, j = chain[0][0]
            ggroup.add(gfxglow.Glow(grid[i][j].rect))
        stage += 1
        
# stage 1
def select(s):
    global chains, stage, grid, board, prevs, moving, captured, dests
    if s in [x[0][0] for x in chains]:
        ggroup.empty()
        rgroup.empty()
        grid.move(prevs, s)
        moving = True
        for i, chain in enumerate(chains):
            if chain[0][0] != s:
                del chains[i]
        if len(chains) > 1:
            for chain in chains:
                if chain:
                    cap = logic.captured(board, prevs, chain[0])
                    for x,y in cap:
                        rgroup.add(gfxring.Ring(grid[x][y].rect))
                    captured.append(cap)
            stage = 2
        elif len(chains) == 1:
            stage = 3
        else:
            player_end_turn()
            return
    else:
        stage = 0
        start(s)

# stage 2
def resolve(s):
    global captured, chains, board
    for i, cap in enumerate(captured):
        if s in cap:
            chains = [chains[i]]
            capture()
            break

# stage 3
def capture():
    global board, prevs, chains
    print prevs, chains[0][0]
    board.remove(logic.captured(board, prevs, chains[0][0]))
    board.move(prevs, chains[0][0][0])
    for i, chain in enumerate(chains):
        del chains[i][0]
        if not chains[i]:
            del chains[i]
    for chain in chains:
        i, j = chain[0]
        ggroup.add(gfxglow.Glow(grid[i][j].rect))
    if chains:
        stage = 1
    else:
        player_end_turn()

def player_end_turn():
    global chains, board, prevs, stage, captured, current
    chains = []
    stage = 0
    prevs = ()
    captured = []
    current = cpu

#def player_movee(mousepos):
#    global lastsel, sel_move, chain, lastdest, startsel, current, resolving, moveit, pending
#    if grid.m:
#        return # currently gfx updating
#    if moveit:
#        moveit = False
#        moves = [m for m in board.moves[lastsel] if m[0] == lastdest]
#        if len(moves) > 1:
#            # player must resolve ambiguity 
#            for m in moves:
#                for x, y in logic.captured(board, lastsel, m):
#                    # add decorations to candidate captures
#                    rgroup.add(gfxring.Ring(grid[x][y].rect))
#            board.moves[lastsel] = moves
#            resolving = True
#            return
#        elif len(moves) == 1:
#            # normal capture
#            captured = logic.captured(board, lastsel, moves[0])
#            board.remove(captured)
#            grid.remove(captured)
#            board.move(lastsel, lastdest)
#            chain.append(lastdest)
#            lastsel = lastdest
#            m = board.moves[lastsel] = logic.refine(board, lastsel, board.adjacent(lastsel), chain)
#            if m:
#                # chain
#                x,y = lastdest
#                rgroup.add(gfxring.Ring(grid[x][y].rect))
#                for move in m:
#                    x,y = move[0]
#                    ggroup.add(gfxglow.Glow(grid[x][y].rect))
#                sel_move = True
#            else:
#                # end turn
#                chain = []
#                current = cpu
#                return
#        else:
#            # paika
#            board.move(lastsel, lastdest)
#            chain = []
#            current = cpu
#            return
#            
#    for i in range(5):
#        for j in range(9):
#            if grid[i][j].rect.collidepoint(mousepos):
#                s = (i,j)
#                
#                if resolving:
#                    for m in board.moves[lastsel]:
#                        if s in logic.captured(board, lastsel, m):
#                            board.moves[lastsel] = [m]
#                            resolving = False
#                            moveit = True
#                            player_move(0)
#                elif sel_move and s in [m[0] for m in board.moves[lastsel]]:
#                    for posmove in [m for m in board.moves[lastsel] if m[0] == s]:
#                        pending.append(posmove)
#                    # selection accepted
#                    # clear all gfx indicators
#                    rgroup.empty()
#                    ggroup.empty()
#                    grid.move(lastsel, s)
#                    chain = [lastsel]
#                    lastdest = s
#                    moving = True
#                    sel_move = False
#                elif s in board.moves and board[i][j] == player:
#                    # add glow to possible moves
#                    for move in board.moves[s]:
#                        x, y = move[0]
#                        ggroup.add(gfxglow.Glow(grid[x][y].rect))
#                    # add decorator ring around selected stone
#                    rgroup.add(gfxring.Ring(grid[i][j].rect))
#                    lastsel = s
#                    sel_move = True

def cpu_move():
    pass

def game_over():
    if board.terminal():
        return True
    return False