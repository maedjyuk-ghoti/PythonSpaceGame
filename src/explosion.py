""" explosion.py/chunk.py """
import pygame
from random import randint
import random

CHUNKS = 16
EXPLODE_SPEED = 0.0


class Chunk(pygame.sprite.Sprite):
    """ Building blocks for an explosion """
    def __init__(self, image, speed, loc):
        """ init """
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = image
        self.rect = image.get_rect()
        self.loc = list(loc)
        self.speed = list(speed)
        self.rect.topleft = self.loc
        self.curr_ticks = pygame.time.get_ticks()

    def update(self):
        """ Updates vars. Should be run every frame. """
        prev_ticks = self.curr_ticks
        self.curr_ticks = pygame.time.get_ticks()
        ticks = self.curr_ticks - prev_ticks
        self.speed[1] += 0.005
        incrx = self.speed[0] * ticks
        incry = self.speed[1] * ticks
        self.loc[0] += incrx
        self.loc[1] += incry
        if self.loc[1] >= self.screen.get_rect().height:
            self.kill()
        self.rect.topleft = self.loc


class Explosion(pygame.sprite.Sprite):
    """ AN EXPLOSION """
    def __init__(self, image, rect, loc, speed):
        """ init """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.loc = list(loc)
        self.speed = speed
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.chunk_group = pygame.sprite.Group()
        self.make_chunks()
        self.done = False

    # Ternary operator: 'a'if 1 == 0 else 'b'
    def make_chunks(self):
        """ Creates chunks of the exploding image """
        num_chunks = CHUNKS
        chunk_width = self.rect.width / num_chunks
        chunk_height = self.rect.height / num_chunks
        img_size = (chunk_width, chunk_height)
        speed = list((0, 0))
        loc = list((0, 0))
        for i in range(num_chunks):
            for j in range(num_chunks):
                speed[0] = (random.random() + EXPLODE_SPEED) *\
                        (-1 if randint(1, 2) == 1 else 1)
                speed[0] += self.speed
                speed[1] = (random.random() + EXPLODE_SPEED) *\
                        (-1 if randint(1, 2) == 1 else 1)
                loc[0] = i * chunk_width
                loc[1] = j * chunk_width
                tmp_img = pygame.Surface(img_size)
                #tmp_img.fill(pygame.Color("magenta"))
                tmp_img.blit(self.image, (0, 0), (loc, img_size))
                tmp_img.set_colorkey(pygame.Color("magenta"))
                self.chunk_group.add(
                        Chunk(tmp_img, speed, (loc[0] + self.loc[0],
                            loc[1] + self.loc[1])))

    def update(self):
        """ Updates vars. Should be run every frame. """
        self.chunk_group.update()
        if len(self.chunk_group) == 0:
            self.done = True

    def draw(self):
        """ draws the explosion on the screen """
        self.chunk_group.draw(self.screen)
