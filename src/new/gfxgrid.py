import pygame
import game
import gfx
import itertools
import gfxtile
import utils
from gfxtile import Square
from constants import *
import board

class Piece:
    """
    Container for the position and image of each stone.
    """
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image
        
               
class Grid:
    """
    Graphical representation of the board.
    """
    def __init__(self, board):
        self.grid = [[], [], [], [], []]
        self.m = ()
        self.initGrid(board)
    
    def move(self, x1, y1, x2, y2):
        """
        Creates a move property used during update.
        x, y == row, column, not screen coordinates.
        """
        self.m = ((x1, y1),(x2, y2))
    
    def update(self):
        """
        Updates ongoing move (if it exists).
        """
        if self.m:
            sx, sy, dx, dy = itertools.chain.from_iterable(self.m)
            start = self.grid[sx][sy]
            dest = self.grid[dx][dy]
            d = utils.tsub((dx,dy),(sx,sy)) # calculate direction
            if start.rect.topleft == dest.rect.topleft:
                # reached destination
                self.grid[dx][dy] = start
                self.grid[sx][sy] = dest
                self.move = ()
            else:
                # keep moving
                start.rect.topleft = utils.tadd(start.rect.topleft, utils.tflip(d))
                    
    def draw(self, screen):
        """
        Draws all the pretty stones on the screen.
        """
        for sq in itertools.chain.from_iterable(self.grid):
            screen.blit(sq.image, sq.rect)
            
    def initGrid(self, board):
        """
        Initialize the pieces at their starting coordinates.
        """
        xs = 90
        ys = 50
        for i in range(5):
            for j in range(9):
                xadd = j*60
                yadd = i*60
                if board[i][j] and board[i][j].color == BLACK:
                    image = BLACK_IMG
                elif board[i][j] and board[i][j].color == WHITE:
                    image = WHITE_IMG
                else:
                    image = NULL_IMG
                self.grid[i].append(Piece(pygame.Rect((xs+xadd, ys+yadd), (60, 60)), image))
            
                                      
# Resources used by this module
BLACK_IMG = None
WHITE_IMG = None
NULL_IMG = None
def load_resources():
    global BLACK_IMG, WHITE_IMG, NULL_IMG
    BLACK_IMG = utils.load_image('black.png')
    WHITE_IMG = utils.load_image('white.png')
    NULL_IMG = utils.load_image('null.png')

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((720, 400))
    load_resources()
    background = utils.load_image('board.jpg')
    g = Grid(board.Board())

    while 1:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                g.move(2,1,2,2)
        screen.blit(background, (0,0))
        g.update()
        g.draw(screen)
        pygame.display.update()