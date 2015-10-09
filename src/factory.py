""" factory.py """
import src.helpers as Helpers


class Factory(object):
    """ Factory class for quick image loads """
    __sprites = {}
    __screen = None

    def __init__(self, screen=None, *args):
        """ init """
        if screen:
            Factory.__screen = screen

        for fnum in args:
            #f[0] = name to refer to it by
            #f[1] = filename
            if isinstance(fnum[1], str):
                #make a sprite for it
                #load it into a dictionary with f[1] as the key
                Factory.__sprites[fnum[0]] = Helpers.load_image(fnum[1])
            else:
                #not a filename, don't care
                pass

    def get_sprite_data(self, key):
        """ returns sprite data """
        try:
            return Factory.__sprites[key]
        except KeyError:
            print(("Key: ", key, "doesn't exist"))

    def get_screen(self):
        """ returns the screen used by factory """
        return Factory.__screen

    def add_sprites(self, *args):
        """ adds sprites to the factory """
        for fnum in args:
            #f[0] = name to refer to it by
            #f[1] = filename
            if isinstance(fnum[1], str):
                #make a sprite for it
                #load it into a dictionary with f[1] as the key
                Factory.__sprites[fnum[0]] = Helpers.load_image(fnum[1])
            else:
                #not a filename, don't care
                pass
