""" menuitem.py """
import pygame


class MenuItem(pygame.font.Font):
    """ A button or thingy in the menu """
    def __init__(self, text, font=None, font_size=30,
            font_color=(255, 255, 255), pos=(0, 0)):
        """ init """
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.position = pos

    def set_position(self, posx, posy):
        """ sets the menuitems location on screen """
        self.position = (posx, posy)

    def is_mouse_selection(self, (posx, posy)):
        """ checks if it is selected by the mouse """
        if (posx >= self.position[0] and
                posx <= self.position[0] + self.width) and\
                (posy >= self.position[1] and
                 posy <= self.position[1] + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        """ sets the font color """
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
