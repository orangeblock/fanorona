import game
import pygame
import gfx

blackImg = None
whiteImg = None
nullImg = None
def load_resources():
    global blackImg, whiteImg, nullImg
    blackImg = gfx.load_image('black.png')
    whiteImg = gfx.load_image('white.png')
    nullImg = gfx.load_image('null.png')
    
class Square(pygame.sprite.Sprite):
    """
    Class representing a grid square on the screen.
    It extends the Sprite class for easier redrawing.
    """
    def __init__(self, x, y, rect, stone = None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = rect
        self.stone = stone
        self.dest = None
        self.delay = 10
        self.lastUpdate = 0
        self._setImg()
    
    # If a new stone replaces current one use setStone() instead.
    def clearStone(self):
        self.stone = None
        self._setImg()
    
    # clearStone() exists only for clearer definition,
    # setStone() also clears when given no arguments.
    def setStone(self, stone = None):
        self.stone = stone
        self._setImg()
    
    def move(self, dest, direction):
        self.dest = dest
        self.direction = direction
        game.moving = True
        
    # set the stone image according to its color
    def _setImg(self):
        if not self.stone:
            self.image = nullImg
        elif self.stone.color is game.WHITE:
            self.image = whiteImg
        elif self.stone.color is game.BLACK:
            self.image = blackImg
            
    def reset(self):
        """ Resets the square's original coordinates """
        self.rect = pygame.Rect( (90 + self.y*60, 50 + self.x*60), (60, 60) )
        
    def update(self, time):
        """ Moves the stone to a new square. """
        if time - self.lastUpdate > self.delay:
            if self.dest != None:
                if self.rect.topleft == self.dest.rect.topleft:
                    # reached destination
                    self.dest.setStone(self.stone)
                    self.clearStone()
                    self.dest = None
                    self.reset()
                    game.moving = False
                    # trigger the logical moving of the stone
                    game.move(self, game.iaxes(self.direction))
                else:
                    # move it one pixel in the direction given
                    self.rect.topleft = game.add_tuple_elements(self.rect.topleft, self.direction)
            self.lastUpdate = time
            