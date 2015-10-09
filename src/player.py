""" player.py """
import pygame
import src.factory as Factory
import src.audio as Audio

MIN_SPIN = 1.0
DELAY = 20


class Player(pygame.sprite.Sprite):
    """ The player sprite """
    def __init__(self):
        """ init """
        pygame.sprite.Sprite.__init__(self)
        self.image_file = "player"
        self.audio_engine = Audio.Audio()

        #Get these from xml
        self.image_size = (60, 30)
        self.frames = 4
        self.speed = list((0, 0))
        self.delta_y = 3
        self.audio_address = "/player"

        #Probably shouldn't touch these
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        self.load_images()
        self.image = self.img_list[0]
        self.rect = self.image.get_rect()
        self.screen = Factory.Factory().get_screen()
        self.screen_rect = self.screen.get_rect()
        self.loc = list((self.rect.width / 2,
                (self.screen_rect.height / 2) - (self.rect.height / 2)))
        self.rect.topleft = self.loc
        self.curr_ticks = pygame.time.get_ticks()
        self.delay = 0
        self.index = 0
        self.moving_up = False

    def load_images(self):
        """ Loads the images that make up the player sprite and its motions """
        img_master = Factory.Factory().get_sprite_data(self.image_file)
        offset = []
        for i in range(self.frames):
            offset.append((i * self.image_size[0], 0))
            tmp_img = pygame.Surface(self.image_size)
            tmp_img.blit(img_master, (0, 0), (offset[i], self.image_size))
            trans_color = tmp_img.get_at((0, 0))
            tmp_img.set_colorkey(trans_color)
            self.img_list.append(tmp_img)

    def move_up(self):
        """ Set movement to up """
        self.moving_up = True

#   def explode(self):
#        """ Goes Boom """
#        print "BOOM!"

    def get_size(self):
        """ returns the size of the player as a tuple """
        return (self.rect.width, self.rect.height)

    def get_loc(self):
        """ returns the location of the player """
        return self.loc

    def draw(self):
        """ Draws the player to the screen """
        self.screen.blit(self.image, (self.loc[0], self.loc[1]))

    def update(self):
        """ Updates all vars. Should be called every frame """
        prev_ticks = self.curr_ticks
        self.curr_ticks = pygame.time.get_ticks()
        ticks = self.curr_ticks - prev_ticks

        incry = self.speed[1] * ticks
        incrx = self.speed[0] * ticks
        self.delay += (abs(incrx) + abs(incry) + MIN_SPIN)
        if self.delay > DELAY:
            self.index = (self.index + 1) % self.frames
            self.delay = 0
        self.image = self.img_list[self.index]

        if self.moving_up:
            self.loc[1] -= self.delta_y
            if self.loc[1] < 0:
                self.loc[1] = 0
            self.moving_up = False
        else:
            self.loc[1] += self.delta_y
            if self.loc[1] > self.screen_rect.height - self.rect.height:
                self.loc[1] = self.screen_rect.height - self.rect.height

        self.rect.topleft = self.loc

        # Add variables to audio bundle
        self.audio_engine.add_to_bundle(self.audio_address + "/speed/x",
            self.speed[0])
        self.audio_engine.add_to_bundle(self.audio_address + "/speed/y",
            self.speed[1])