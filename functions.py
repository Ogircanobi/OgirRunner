import pygame


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
    start_speed = 5  # Initial speed.
    speed_increment = 0.06  # Rate of speed increase
    # Increase speed based on score
    return start_speed + (speed_increment * score)

# scroll_ground scrolls ground across screen
# arguments: screen, ground_surface, ground_x, speed
def scroll_ground(screen, ground_surface, ground_x, speed):
    # Calculate width of ground surface image and display it
    width = ground_surface.get_width()
    screen.blit(ground_surface, (ground_x, 300))

    # Calculate the distance to move ground based on speed
    ground_x -= speed-(speed * 25 / 100)
    # Reset ground_x when image reaches its end
    if ground_x < -width+800:
        ground_x = 0
    return ground_x
