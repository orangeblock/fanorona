import pygame
import gfx

images = []
def load_resources():
    for i in range(8):
        images.append(gfx.load_image('glow/glow{}.png'.format(i)))
        
class Glow(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.index = 0
        self.direction = +1 # fade in / fade out
        self.image = images[self.index]
        self.lastUpdate = pygame.time.get_ticks()
        self.delay = 75 # milliseconds
        
    def update(self, time):
        if time - self.lastUpdate > self.delay:
            self.index += 1*self.direction
            if self.index == len(images)-1 or self.index == 0:
                self.direction = -1*self.direction # change direction
            self.image = images[self.index]
            self.lastUpdate = time