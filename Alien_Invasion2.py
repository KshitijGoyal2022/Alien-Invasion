import pygame
from pygame.sprite import Group

from settings2 import Settings
from ship2 import Ship
import game_functions2 as gf
from game_stats2 import GameStats
from button2 import Button
from scoreboard2 import Scoreboard
from sounds2 import Sound
from powerups2 import overall as powerup


def run_game():
    #Initialize the game and create a screen object
    pygame.init()


# define the initial countdown timer
    countdown_timer = 5000
    countdown_event = pygame.USEREVENT + 1

# create a timer that triggers every 10 seconds
    pygame.time.set_timer(countdown_event, 5000,1000)

    game_settings = Settings()

    screen  = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION")

    ship = Ship(game_settings,screen)
    stats  = GameStats(game_settings)
    play_button = Button(game_settings,screen,"Play")
    sb = Scoreboard(game_settings,screen,stats)
    sound = Sound()
    pup = powerup(screen)


    bullets = Group()
    aliens = Group()

    gf.create_fleet(game_settings,screen,ship,aliens)

    pygame.mixer.music.load('sounds/backgroundmusic1.mp3')
    pygame.mixer.music.play(-1)


    while True:
        gf.check_events(game_settings, screen, stats, sb, play_button, ship, aliens, bullets, pup,countdown_event)
        countdown_timer -=1
        if countdown_timer == 0:
            countdown_timer = 5000
            gf.generate_powerup(pup)

        if stats.game_active:
            if (pup.powerup_active):
                pup.update()

            ship.update()
            gf.update_bullets(game_settings,screen,stats,sb,ship,bullets,aliens,sound)
            gf.update_aliens(game_settings,stats,screen,sb, ship,aliens,bullets)
        gf.update_screen(game_settings,screen,stats,sb,ship,aliens,bullets,play_button,pup)

        #Testing pull


run_game()
pygame.quit()



