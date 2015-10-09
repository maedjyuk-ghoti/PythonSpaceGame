""" helpers.py """
import sys
import os
import pygame
import pygame.locals

WIDTH = 640
HEIGHT = 480
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PALE_BLUE = (153, 204, 255)
SKY_BLUE = (0, 204, 255)
BLACK = (0, 0, 0)


def load_image(name, colorkey=None):
    """ Loads an image from a file """
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(('Cannot load image:', fullname))
        raise SystemExit(message)
    if ".png" in fullname:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image

if __name__ == '__main__':
    pygame.init()
    SCREEN = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Helpers Test')
    if len(sys.argv) != 2:
        print(("usage: ", sys.argv[0], " <file to load>"))
        sys.exit()
    else:
        pygame.init()
        load_image(sys.argv[1])
        #print "Can't test load_image until pygame.display is init"
