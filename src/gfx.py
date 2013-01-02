import gfxtile, gfxring, gfxglow
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

def init():
    global screen, background, font
    screen = pygame.display.set_mode(size)
    background = load_image('board.jpg')
    font = pygame.font.SysFont('Source Code Pro 9', 20)
    gfxtile.load_resources()
    gfxring.load_resources()
    gfxglow.load_resources()

def move(start, end, direction):
    start.move(end, direction)
    
def update():
    # clear everything
    screen.blit(background, (0,0))
    # update the groups in the right order
    gupdate(game.rgroup)
    gupdate(game.sgroup)
    gupdate(game.ggroup)
    # display fps
    tupdate("FPS: " + str(game.clock.get_fps()), (40, 370))
    pygame.display.update()

# updates and redraws given sprite group              
def gupdate(group):
    if len(group) > 0:
        group.update(pygame.time.get_ticks())
        group.draw(screen)
        
# draws text on the location given on the screen
def tupdate(text, location):
    screen.blit(font.render(text, 4, (255,255,255)), location)
    
def load_image(path):
    return pygame.image.load(path).convert_alpha()