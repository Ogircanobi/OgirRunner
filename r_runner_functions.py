import pygame


# Function that displays score on screen
def display_score(start_time, test_font, screen):
    current_time = int(pygame.time.get_ticks()/1000) - start_time  # gets current time/resets start time when you die.
    score_surf = test_font.render(f'Score: {current_time}', False, (0, 204, 102))  # new surface for score
    score_rect = score_surf.get_rect(center=(400, 50))  # rectangle for score_surf
    screen.blit(score_surf, score_rect)  # Draw out on screen
    return current_time


def collision_sprite(player, obstacle_group):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True
