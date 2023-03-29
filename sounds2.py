
import pygame

pygame.mixer.music.set_volume(0.2)

class Sound:
    def __init__(self):
        self.collision_sound = pygame.mixer.Sound('sounds/collision.wav')
        self.collision_sound.set_volume(0.1)
        self.background_sound = pygame.mixer.Sound('sounds/backgroundmusic1.wav')
        # self.background_sound.set_volume((0.6))


