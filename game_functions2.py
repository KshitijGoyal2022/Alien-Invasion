import sys
import threading


import pygame
import pygame.font
import random
from time import sleep


from bullet2 import Bullet
from aliens2 import Alien

pygame.mixer.init()

def check_events(game_settings,screen,stats,sb,play_button,ship,aliens,bullets,pup,countdown_event):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(pup)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,game_settings,screen,ship,bullets,pup)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        else:
            pass

def check_play_button(game_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_click = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_click and stats.game_active==False:
        game_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_settings,screen,ship,aliens)
        ship.center_ship()

def check_keydown_events(event,game_settings,screen,ship,bullets,pup):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        quit_game(pup)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(game_settings,screen,stats,sb,ship,bullets,aliens,sound):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(game_settings,screen,stats,sb,ship,bullets,aliens,sound)

def check_bullet_alien_collisions(game_settings,screen,stats,sb,ship,bullets,aliens,sound):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #collison = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if(collision):
        pygame.mixer.Sound.play(sound.collision_sound)
        for aliens in collision.values():
            stats.score +=game_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_scores(stats,sb)
    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_speed()
        stats.level+=1
        change_level(game_settings,screen,stats,sb)
        sb.prep_level()
        create_fleet(game_settings, screen, ship, aliens)

def update_screen(game_settings,screen,stats,sb,ship,aliens,bullets,play_button,pup):
    screen.fill(game_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen) #Groups can use the draw function to draw everything inside
    sb.show_score()

    if pup.powerup_active:
        pup.blit_powers()

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def change_level(game_settings,screen,stats,sb):
    screen.fill(game_settings.bg_color)
    screen_rect = screen.get_rect()
    level_str = "Level "+str(stats.level)
    level_image = pygame.font.SysFont(None,48).render(level_str,True,sb.text_color,game_settings.bg_color)
    level_image_rect = level_image.get_rect()
    level_image_rect.x = screen_rect.x
    level_image_rect.center = screen_rect.center
    sb.show_change_level(level_image,level_image_rect)
    pygame.display.flip()
    sleep(2)

def fire_bullets(game_settings, screen, ship, bullets):
    if len(bullets) < game_settings.bullet_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(game_settings,alien_width):

    available_space_x = game_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(game_settings,ship_height,alien_height):
    available_space_y = (game_settings.screen_height-(3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_fleet(game_settings,screen,ship,aliens):
    alien = Alien(game_settings,screen)
    number_aliens_x = get_number_aliens_x(game_settings,alien.rect.width)
    number_of_rows = get_number_rows(game_settings,ship.rect.height,alien.rect.height)

    for row_number in range(number_of_rows-3):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings,screen,aliens,alien_number,row_number)

def create_alien(game_settings,screen,aliens,alien_number,row_number):#,row_number

        alien = Alien(game_settings,screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 1.5* alien.rect.height + 2 * alien.rect.height * row_number +40
        aliens.add(alien)

def check_fleet_edges(game_settings,aliens):
    for alien in aliens.sprites():
        if (alien.check_edges()):
            change_fleet_direction(game_settings,aliens)
            break

def change_fleet_direction(game_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *=-1

def update_aliens(game_settings,stats,screen,sb,ship,aliens,bullets):
    check_fleet_edges(game_settings,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(game_settings,stats,screen,sb,ship,aliens,bullets)
    check_aliens_bottom(game_settings,stats,screen,sb,ship,aliens,bullets)

def ship_hit(game_settings,stats,screen,sb,ship,aliens,bullets):
    if stats.ships_left>1:
        stats.ships_left-=1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        with open("highscore.txt","w") as hs:
            hs.write(str(stats.high_score))

        stats.game_active = False

def check_aliens_bottom(game_settings,stats,screen,sb,ship,aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(game_settings,stats,screen,sb,ship,aliens,bullets)
            break

def check_high_scores(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

timer_threads = []
def generate_powerup(pup):
    # scheduler.enter(10,1,generate_powerup,(pup,scheduler,))

    pup.powerup_active = True

    p = random.randint(0,6)
    match p:
        case 0:
            pup.initialize_powerup(pup.triple_bullet)
        case 1:
            pup.initialize_powerup(pup.complete_wipe)
        case 2:
            pup.initialize_powerup(pup.ship_speed_up)
        case 3:
            pup.initialize_powerup(pup.double_points)
        case 4:
            pup.initialize_powerup(pup.ship_slow_down)
        case 5:
            pup.initialize_powerup(pup.deduct_points)

def quit_game(pup):
    pup.powerup_active = False
    sys.exit()
























