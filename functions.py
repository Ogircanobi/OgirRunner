import pygame
import math
import time

# Function that displays score on screen
def display_score(start_time, test_font, screen):
    current_time = int(pygame.time.get_ticks()/1000) - start_time  # gets current time/resets start time when you die.
    score_surf = test_font.render(f'Score: {current_time}', False, (0, 204, 102))  # new surface for score
    score_rect = score_surf.get_rect(center=(400, 50))  # rectangle for score_surf
    screen.blit(score_surf, score_rect)  # Draw out on screen
    return current_time


# collision detection function
def collision_sprite(player, obstacle_group):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# This function adjusts speed of enemies based on score
def speed_update(score):
    start_speed = 10  # Initial speed.
    speed_increment = 0.08  # Rate of speed increase
    # Increase speed based on score
    return start_speed + (speed_increment * score)


# scroll_ground scrolls ground across screen
# arguments: screen, ground_surface, ground_x, speed
def scroll_ground(screen, ground_surface, ground_x, speed):
    # Calculate width of ground surface image and display it
    width = ground_surface.get_width()
    tiles = math.ceil(800/width) + 1
    for i in range(0, tiles):
        screen.blit(ground_surface, (i * width + ground_x, 300))
    # Ground movement calcuation is 25% slower than enemy speed.
    ground_x -= speed-(speed * 25 / 100)
    # Reset ground_x when image reaches its end
    if abs(ground_x) > width:
        ground_x = 0
    return ground_x


def scroll_sky(screen, sky_x, speed, sky_surfaces):

    # define how many tiles needed to fill screen:
    bg_width = sky_surfaces[0].get_width() * len(sky_surfaces)

    # scroll position 90% slower than enemy speed
    sky_x -= (speed-(speed * 90 / 100))

    # Reset scroll (check if scroll variable is greater than width of image)
    if abs(sky_x) > bg_width - 800:
        sky_x = 0

    # Blit multiple tiles on screen
    for i in range(len(sky_surfaces)):
        screen.blit(sky_surfaces[i], (i * 800 + sky_x, 0))

    return sky_x


def scroll_wall(screen, speed, wall_x, reset_wall_x, wall_surfaces):
    # Check if reset_wall_x is True. This means that
    # the skies have finished transitioning and scroll_wall will no longer be called.
    # We should reset wall_x at this point to prepare for the next call.
    if reset_wall_x:
        wall_x = 800
        reset_wall_x = False
    # Calculate scroll position 90% slower than enemy speed
    wall_x -= (speed-(speed * 25 / 100))

    # Blit multiple tiles on screen
    for i in range(len(wall_surfaces)):
        screen.blit(wall_surfaces[i], (i * 800 + wall_x, 0))

    return wall_x, reset_wall_x
