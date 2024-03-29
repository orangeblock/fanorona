import gfxgrid, gfxring, gfxglow
import pygame
import game

# window size
size = width, height = 720, 400

# where everything gets displayed
screen = None

# the board background
background = None

# text font
font = None
text = None

def init():
    global screen, background, font
    screen = pygame.display.set_mode(size)
    background = load_image('board.jpg')
    font = pygame.font.SysFont('Times New Roman', 20)
    gfxgrid.load_resources()
    gfxring.load_resources()
    gfxglow.load_resources()

def move(start, end, direction):
    start.move(end, direction)
    game.grid.move()
    
def update():
    # clear everything
    screen.blit(background, (0,0))
    # update the groups in the right order
    gupdate(game.rgroup)
    gupdate(game.ggroup)
    game.grid.update()
    game.grid.draw(screen)
    # display fps
    tupdate(text, (330, 190))
    pygame.display.update()

# updates and redraws given sprite group              
def gupdate(group):
    if len(group) > 0:
        group.update(pygame.time.get_ticks())
        group.draw(screen)
        
# draws text on the location given on the screen
def tupdate(text, location):
    screen.blit(font.render(text, 50, (255,255,255)), location)
    
def load_image(path):
    return pygame.image.load(path).convert_alpha()