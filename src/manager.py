""" manager.py """
import pygame
import sys
import src.menu as Menu
import src.inputbox as Inputbox
import src.gamemanager as Gamemanager

pygame.init()


class Manager(object):
    """ Manages the state of the program """
    def __init__(self):
        """ init """
        #Pygame initial stuffs
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Game (in progress)')
        self.ticks = pygame.time.get_ticks()
        self.views = None
        self.curr_view = None
        self.clock = pygame.time.Clock()

    def set_view(self, view):
        """ Sets the menu view """
        if view == 'Back':
            view = 'Main Menu'
        self.curr_view = view

    def add_menuitem(self, menu, item_key):
        """ adds an item to the menu """
        self.views[menu].add_menuitem(item_key, self.placeholder)
        self.set_view(menu)

    def quit_game(self, item_key):
        """ quits the game """
        print("'Quit' was clicked")
        sys.exit()

    def start_game(self, item_key):
        """ begins the game """
        print("Starting Game!")

    def placeholder(self, *args):
        """ a placeholder """
        print(("Placeholder function called from", args))

    def play(self):
        """ the meat of the program """
        #Menus
        main_menu_funcs = {'Start': self.set_view,
                'High Scores': self.set_view,
                'Options': self.set_view,
                'Quit': self.quit_game}
        main_menu = Menu.Menu(self.screen,
                    list(main_menu_funcs.keys()),
                    main_menu_funcs)

        options_menu_funcs = {'Controls': self.set_view,
                    'Back': self.set_view}
        options_menu = Menu.Menu(self.screen,
                    list(options_menu_funcs.keys()),
                    options_menu_funcs)

        controls_menu_funcs = {'Up: Up Arrow': self.placeholder,
                    'Shoot: Space Bar': self.placeholder,
                    'Back': self.set_view}
        controls_menu = Menu.Menu(self.screen,
                    list(controls_menu_funcs.keys()),
                    controls_menu_funcs)

        highscore_menu_funcs = {'Name': self.set_view,
                    'Back': self.set_view}
        highscore_menu = Menu.Menu(self.screen,
                    list(highscore_menu_funcs.keys()),
                    highscore_menu_funcs)

        #Inputbox for High Scores menu, called when 'Name' is clicked
        name_input_box = Inputbox.Inputbox(self.screen, self.add_menuitem,
                        "High Scores", "Name")

        the_game = Gamemanager.GameManager(self.screen)

        #Workload
        # Note 1: I don't like hardcoding "Main Menu" as the default curr_view,
        #  but the first menu should be the main menu so it doesn't matter.
        #  Just make sure there is a "Main Menu" in self.views
        #
        # Note 2: These are the views that can be selected by the set_view()
        #  function these are not all the buttons available
        self.views = {'Main Menu': main_menu,
                'Options': options_menu,
                'High Scores': highscore_menu,
                'Name': name_input_box,
                'Start': the_game,
                'Controls': controls_menu}

        mainloop = True
        self.curr_view = "Main Menu"
        #This is the one loop to rule them all.
        # This should pretty much be the last line,
        # any setup for the game should be above this.
        while mainloop:
            self.clock.tick(60)
            self.views[self.curr_view].display()
            mainloop = self.views["Main Menu"].mainloop

if __name__ == "__main__":
    MANAGER = Manager()
    MANAGER.play()
