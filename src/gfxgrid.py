import pygame
import game
import itertools
import utils
from constants import *
import board
import copy

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
        self.m = []
        self.initGrid(board)
    
    def __getitem__(self, index):
        return self.grid[index]
    
    def __setitem__(self, key, value):
        self.grid[key] = value
        
    def move(self, pos1, pos2):
        """
        Creates a move property used during update.
        x, y == row, column, not screen coordinates.
        """
        self.m = [pos1, pos2]
        self.original = copy.deepcopy(self[pos1[0]][pos1[1]].rect)
    
    def update(self):
        """
        Updates ongoing move (if it exists).
        """
        if self.m:
            sx, sy, dx, dy = itertools.chain.from_iterable(self.m)
            start = self[sx][sy]
            dest = self[dx][dy]
            d = utils.tsub((dx,dy),(sx,sy)) # calculate direction
            if start.rect.topleft == dest.rect.topleft:
                # reached destination
                self[sx][sy].rect = self.original
                self[dx][dy].image = self[sx][sy].image
                self[sx][sy].image = NULL_IMG
                self.m = []
                game.moving = False
                if game.current == game.player:
                    game.move()
            else:
                # keep moving
                start.rect.topleft = utils.tadd(start.rect.topleft, utils.tflip(d))
    
    def remove(self, positions):
        for x,y in positions:
            self[x][y].image = NULL_IMG
                
    def draw(self, screen):
        """
        Draws all the pretty stones on the screen.
        """
        for sq in itertools.chain.from_iterable(self.grid):
            screen.blit(sq.image, sq.rect)
    
    def collision(self, mousepos):
        """
        Returns the position of the stone that collides
        with the mouse, None otherwise.
        """
        for i in range(5):
            for j in range(9):
                if self[i][j].rect.collidepoint(mousepos):
                    return (i,j)
        return None
            
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
                if board[i][j] == BLACK:
                    image = BLACK_IMG
                elif board[i][j] == WHITE:
                    image = WHITE_IMG
                else:
                    image = NULL_IMG
                self[i].append(Piece(pygame.Rect((xs+xadd, ys+yadd), (60, 60)), image))
            
                                      
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
                g.move((2,1),(2,2))
        screen.blit(background, (0,0))
        g.update()
        g.draw(screen)
        pygame.display.update()