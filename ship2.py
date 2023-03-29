import pygame
from pygame.sprite import Sprite
class Ship(Sprite):

    def __init__(self,game_settings,screen):
        super(Ship,self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        self.image = pygame.image.load('images/ship2.png')
        self.image = pygame.transform.scale(self.image, (70,52))

        # self.ships_left_image = pygame.image.load('images/ship2.png')
        # self.ships_left_image = pygame.transform.scale(self.ships_left_image,(50,37))
        # self.ships_left_image_rect = self.ships_left_image.get_rect()

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def blitme(self):

        self.screen.blit(self.image,self.rect)

    def update(self):
        if self.moving_right and self.rect.right<=self.screen_rect.right:
            self.center +=self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left>=0:
            self.center-=self.game_settings.ship_speed_factor
        self.rect.centerx =self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx