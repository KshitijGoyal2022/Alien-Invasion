import pygame
import random

class overall():
    def __init__(self,screen):
        self.screen = screen
        screen_rect = self.screen.get_rect()

        self.triple_bullet = pygame.image.load('powerups/triple_bullet.png')
        self.complete_wipe = pygame.image.load('powerups/complete_wipe.png')
        self.ship_speed_up = pygame.image.load('powerups/speed.png')
        self.double_points = pygame.image.load('powerups/score_multiplier.png')
        self.ship_slow_down = pygame.image.load('powerups/slow_down.png')
        self.deduct_points = pygame.image.load('powerups/point_deduction.png')

        self.powerup_active = False

    def initialize_powerup(self,powerup_image):
        self.powerup_image = powerup_image
        self.powerup_image = pygame.transform.scale(self.powerup_image, (35, 35))
        self.powerup_image_rect = self.powerup_image.get_rect()
        self.powerup_image_rect.x = random.randint(20,1151)
        self.powerup_image_rect.y = 40

    def blit_powers(self):
        self.screen.blit(self.powerup_image,self.powerup_image_rect)

    def update(self):
        self.powerup_image_rect.y +=1

        if(self.powerup_image_rect.y > 750):
            self.powerup_active = False

        '''
        Done:Use inheritance. 
        Done: Make a new class that has a function to do getrect().

        Done: In that class, it should also have an update function that works 
        Done: by changing the y value of the image by a certain amount as declared in game_settings.py

        Done: Lastly, it should have a draw function that blits these images onto the screen and continuously changes them.

        First half done: Find a way to randomize powerup chosen and how often it is done. 
        
        This can be done by using the sprite class so that we check whether the bullet and the powerup collide. If collision takes place
        we call the change_settings part of the game

        Lastly, add functionality for each power up, on how it changes the settings of the game. 
        '''
