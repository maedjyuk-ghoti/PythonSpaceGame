""" bullet.py """
import pygame
import src.factory as Factory


class Bullet(pygame.sprite.Sprite):
    """ A class to control a bullet that flies across screen """
    def __init__(self):
        """ init """
        pygame.sprite.Sprite.__init__(self)
        self.image_key = "bullet"

        #Get these from xml
        self.image_size = (10, 4)
        self.speed = list((10, 0))

        #Probably shouldn't touch these
        self.image = Factory.Factory().get_sprite_data(self.image_key)
        self.rect = self.image.get_rect()
        self.screen = Factory.Factory().get_screen()
        self.screen_rect = self.screen.get_rect()
        self.on_screen = False

        self.loc_coord = list((0, 0))

    def get_size(self):
        """ Returns the size of the bullet hitbox as a tuple """
        return (self.rect.width, self.rect.height)

    def draw(self):
        """ Draws the bullet to the screen at x_coord, y_coord """
        self.screen.blit(self.image, self.loc_coord)

    def update(self):
        """ Updates the position of the bullet. Should be called every frame"""
        self.loc_coord[0] += self.speed[0]
        self.rect.topleft = self.loc_coord
        if self.loc_coord[0] > (self.screen_rect.width - self.rect.width):
            self.on_screen = False

    def hit(self):
        """ Function used when bullet hits something.
            Teleports bullet offscreen """
        self.on_screen = False
        self.loc_coord[0] += self.screen_rect.width
        self.loc_coord[1] += self.screen_rect.height

    def shoot(self, loc):
        """ starts a bullet moving across the screen using the coordinates from
            the 'loc' tuple """
        self.on_screen = True
        self.loc_coord = list(loc)

    def is_on_screen(self):
        """ Checks if the bullet is currently in the viewing area """
        return self.on_screen

    def audio_report(self):
        """ reports the message and var to audio engine for osc messages """
