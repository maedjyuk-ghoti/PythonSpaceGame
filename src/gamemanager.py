""" gamemanager.py """
import sys
import pygame
from numpy import random
import src.player as Player
import src.parallax as Parallax
import src.bullet as Bullet
import src.factory as Factory
import src.mine as Mine
import src.explosion as Explosion
import src.audio as Audio


class GameManager(object):
    """ Manages game objects and states """
    def __init__(self, screen):
        """ init """
        self.screen = screen
        self.ticks = pygame.time.get_ticks()
        pygame.mouse.set_visible(False)
        self.audio_engine = Audio.Audio()
        self.elapsed = 0
        self.delay = 5
        self.cur_ticks = pygame.time.get_ticks()
        self.keys = pygame.key.get_pressed()
        self.frames = 0
        self.first_run = True

        #These need to be changeable through options menu eventually
        self.player_key_up = pygame.K_UP
        self.player_key_shoot = pygame.K_SPACE

        self.factory = Factory.Factory(screen, ("player", "player_star.png"),
                ("bullet", "bullet.png"), ("mine", "brown_mine.png"))

        self.background = Parallax.ParallaxSurface((640, 480))
        self.background.add("images/background_far.png", 2)
        self.background.add("images/background_close.png", 1)

        self.explosions = []

        self.player = Player.Player()

        #Bullet stuffs (with pooling)
        self.bullets = []
        self.bullet_delay = 300
        self.bullet_cur_ticks = self.cur_ticks
        self.bullet_elapsed = 0

        #Enemy creation
        self.enemy_group = pygame.sprite.Group()
        self.num_enemies = 0
        while self.num_enemies < random.randint(20, 40):
            self.num_enemies += 1
            self.enemy_group.add(Mine.Mine(list((random.randint(960, 1560),
                        random.randint(20, 460))),
                        list((random.randint(-7, 0), 0))))

    def on_exit(self):
        """ Function to perform at end of program """
        ticks = pygame.time.get_ticks() - self.ticks
        print("GAME OVER")
        print(("mines:", self.num_enemies))
        print(("frames:", self.frames))
        print(("ticks:", ticks))
        print(("fps:", self.frames / (ticks * 0.001)))
        self.first_run = True
        self.audio_engine.quit_server()
        # Save whatever needs saving from the gamescreen (score most likely)
        # need a way to go back to the main menu or just stop entirely
        # in a more glorious/graceful way than the this
        sys.exit()

    def shoot(self):
        """ Performs all creation and procedures needed to shoot a bullet """
        prev_ticks = self.bullet_cur_ticks
        self.bullet_cur_ticks = pygame.time.get_ticks()
        ticks = self.bullet_cur_ticks - prev_ticks
        self.bullet_elapsed += ticks
        if self.bullet_elapsed > self.bullet_delay:
            fired = False
            player_loc = self.player.get_loc()
            player_size = self.player.get_size()
            player_mid_right = ((player_loc[0] + player_size[0]),
                    (player_loc[1] + (player_size[1] / 2)))

            for bul in self.bullets:
                if not bul.is_on_screen():
                    b_size = bul.get_size()
                    b_loc = ((player_mid_right[0] - (b_size[0] / 2)),
                        (player_mid_right[1] - (b_size[1] / 2)))
                    bul.shoot(b_loc)
                    fired = True
                    break

            if not fired:
                bul = Bullet.Bullet()
                b_size = bul.get_size()
                b_loc = ((player_mid_right[0]),
                    (player_mid_right[1] - (b_size[1] / 2)))
                bul.shoot(b_loc)
                self.bullets.append(bul)
            self.bullet_elapsed = self.bullet_elapsed % self.bullet_delay

    def display(self):
        """ Called from manager, handles draws and updates of all assets """
        if self.first_run:
            self.ticks = pygame.time.get_ticks()
            self.first_run = False

        # Check for exit key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.on_exit()

        # Update tick count
        prev_ticks = self.cur_ticks
        self.cur_ticks = pygame.time.get_ticks()
        ticks = self.cur_ticks - prev_ticks
        self.elapsed += ticks
        if self.elapsed > self.delay:
            self.elapsed = self.elapsed % self.delay
            self.keys = pygame.key.get_pressed()

        # Check for player input we can use
        if self.keys[self.player_key_up]:
            self.player.move_up()
        if self.keys[self.player_key_shoot]:
            self.shoot()
            self.audio_engine.send_message("/shotsfired")

        # Update all the things
        self.background.scroll(2)
        self.player.update()
        self.enemy_group.update()
        for bul in self.bullets:
            if bul.is_on_screen:
                bul.update()

        # Send new audio bundle out
        self.audio_engine.send()

        # Draw all the things
        self.background.draw(self.screen)
        self.player.draw()
        self.enemy_group.draw(self.screen)

        # Handle a collision with player if it happened
        if pygame.sprite.spritecollide(self.player, self.enemy_group, True):
            self.audio_engine.send_message("/explosion")
            print("YOU WERE HIT")
            self.on_exit()

        # Handle a bullet hitting an object
        for bul in self.bullets:
            if bul.is_on_screen:
                bul.draw()
                enemies = pygame.sprite.spritecollide(bul,
                        self.enemy_group, True)
                if enemies:
                    bul.hit()
                    for enemy in enemies:
                        exploded = Explosion.Explosion(enemy.image,
                            enemy.rect, (enemy.loc[0], enemy.loc[1]),
                            enemy.speed[0] / 4.0)
                        self.explosions.append(exploded)
                        self.audio_engine.send_message("/explosion")
        if len(self.explosions):
            for exploding in self.explosions:
                exploding.update()
                exploding.draw()

        # Check number of enemies
        if not len(self.enemy_group):
            temp_explosions = []
            for exploding in self.explosions:
                if not exploding.done:
                    temp_explosions.append(exploding)
            self.explosions = temp_explosions
            if not len(self.explosions):
                print("YOU WIN")
                self.on_exit()

        # Reset for next frame
        pygame.display.flip()
        self.frames += 1


if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode((640, 480))
    SCREEN.set_caption('GameManager Test')
    GAMEMANAGER = GameManager(SCREEN)
    CLOCK = pygame.time.Clock()
    while True:
        CLOCK.tick(60)
        GAMEMANAGER.display()
