import pygame
import gfx


images = []
def load_resources():
    for i in range(11):
        images.append(gfx.load_image('ring/ring{}.png'.format(i)))

class Ring(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.index = 0
        self.image = images[self.index]
        self.lastUpdate = pygame.time.get_ticks()
        self.delay = 80 # milliseconds
        
    def update(self, time):
        if time - self.lastUpdate > self.delay:
            self.index += 1
            if self.index >= len(images):
                self.index = 0
            self.image = images[self.index]
            self.lastUpdate = time
        
    