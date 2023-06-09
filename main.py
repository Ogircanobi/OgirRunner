# Rigoberto Alvarez
# First pygame project
# Started 05/23/2023
# Completed following youTube tutorial: https://www.youtube.com/watch?v=AY9MnQ4x3zk
# credit for martian art: https://opengameart.org/content/martian-walking,
# https://opengameart.org/content/mars-background-pixel-art
import pygame
from sys import exit
from random import choice
import sprites
from functions import display_score, collision_sprite, speed_update, scroll_ground, scroll_sky, scroll_wall

pygame.init()  # Create window using .init() This starts pygame and initiates all necessary functions
# Provide Display Surface below(The window player sees).
screen = pygame.display.set_mode((800, 400))  # set_mode needs at least one argument that represents width,height
pygame.display.set_caption('Rigo Runner')  # set title of game
clock = pygame.time.Clock()  # create clock object to control frame rate
# create a font using .Font(font type, font size) using fonts from font folder
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # 'None' = default font.
game_active = False
start_time = 0
score = 0
ground_x = 0  # starting point of ground graphic
sky_x = 0  # starting point of sky
wall_x = 800  # starting point of walls (off screen)
reset_wall_x = True # setting reset_wall_x: True means its time to show walls
bg_music = pygame.mixer.Sound('audio/music.wav')  # load music
bg_music.play(loops=-1)  # Play music. -1 loops music forever

# Groups (Collections of sprites)
player = pygame.sprite.GroupSingle()  # player  group is a GroupSingle
player.add(sprites.Player())
obstacle_group = pygame.sprite.Group()  # creating group of obstacles

# Setting sky and ground surfaces
# Create list of image file paths for skies and walls
# https://opengameart.org/art-search?keys=sci+fi+wall
skies = [
         'graphics/Skies/marsclose.png',
         'graphics/Skies/marsclose.png',
         'graphics/Skies/marsmid.png',
         'graphics/Skies/marsmid.png',
         'graphics/Skies/marsfar.png',
         'graphics/Skies/marsfar.png',
         'graphics/Skies/marsmountain.png',
         'graphics/Skies/marsmountain.png',
         'graphics/Skies/marsclose.png',
         'graphics/Skies/marsclose.png'
         ]
# set limits for sky transitions to be masked by wall transitions
# Lower limit is the point at which a Skies surface is about to change
# Upper limit is the point at which the transition between skies is done
# This will allow us to blight the walls to cover the transition so player does not see break in picture.
# sky_limits = (lower limit, upper limit)
sky_limits = [(800, 1650), (2400, 3250), (4000, 4850), (5600, 6400)]
# list of wall pictures
walls = ['graphics/SciFi walls/wall_metal1.png',
         'graphics/SciFi walls/wall_metal2.png',
         'graphics/SciFi walls/wall_metal3.png',
         'graphics/SciFi walls/wall_metal4.png',
         'graphics/SciFi walls/wall_metal5.png',
         'graphics/SciFi walls/wall_metal6.png',
         'graphics/SciFi walls/wall_metal7.png'
         ]
# load the background surfaces into a list and convert them BEFORE game loop
# to prevent slowing down game.
sky_surfaces = []
for sky_path in skies:
    sky_surface = pygame.image.load(sky_path).convert()
    sky_surface = pygame.transform.scale(sky_surface, (800, 300))  # Scaling picture
    sky_surfaces.append(sky_surface)

wall_surfaces = []
for wall_path in walls:
    wall_surface = pygame.image.load(wall_path).convert()
    wall_surface = pygame.transform.scale(wall_surface, (800, 300))
    wall_surfaces.append(wall_surface)


ground_surface = pygame.image.load('graphics/Grounds/red_dirt_extend.png').convert()
# Only scale ground surface if necessary:
#ground_surface = pygame.transform.scale(ground_surface, (800, 168))
#ground_surface = ground_surface.convert()

# Intro screen
player_stand = pygame.image.load('graphics/Player/Martian/1.png').convert_alpha()  # importing intro image of player
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # scaling image with rotozoom (making it bigger)
player_stand_rect = player_stand.get_rect(center=(400, 200))  # Create rectangle and setting on screen
game_name = test_font.render('Ogirs Run', False, (111, 196, 169))  # setting game name and color
game_name_rect = game_name.get_rect(center=(400, 80))  # creating rectangle for game_name
game_message = test_font.render('Press space to run', False, (111, 196, 169))  # setting message to start game
game_message_rect = game_message.get_rect(center=(400, 340))  # rectangle for game_message
# Timer
obstacle_timer = pygame.USEREVENT + 1  # always include + 1 when creating a custom user event (see documentation)
pygame.time.set_timer(obstacle_timer, 1500)  # trigger customer event above at certain intervals

##############################################################################################
# Entire game runs here inside while True loop
while True:
    # EVENT LOOP that checks for all possible types of player input using .event.get()
    for event in pygame.event.get():
        # Event to detect player closing the window.
        if event.type == pygame.QUIT:  # .QUIT is a constant synonymous with pressing x button of window
            pygame.quit()  # essentially the opposite of .init()
            exit()  # exit method from sys cancels all code running
        if game_active:
            if event.type == obstacle_timer:  # At set obstacle timer time, add enemies group
                obstacle_group.add(sprites.Obstacle(choice(['fly', 'ground', 'ground', 'ground'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:  # Draw all our elements
        # Update speed based on score
        speed = speed_update(score)
        # Call sky scrolling function
        sky_x = scroll_sky(screen, sky_x, speed, sky_surfaces)
        print(sky_x)
        # This loop checks if it is time to mask sky transition with wall graphics by looping
        # through the sky_limits list.
        # The sky_limits are set on line 55 and consist of upper an lower limits of when to call scroll_wall() function.
        # This times the calling of scroll_() function to coincide with the change of sky background, to mask the
        # transition from the player.
        for lower_limit, upper_limit in sky_limits:
            if lower_limit <= abs(sky_x) <= upper_limit:
                wall_x, reset_wall_x = scroll_wall(screen, speed, wall_x, reset_wall_x, wall_surfaces)
                break
        else:
            reset_wall_x = True

        # Call Ground scrolling function
        ground_x = scroll_ground(screen, ground_surface, ground_x, speed)
        score = display_score(start_time, test_font, screen)
        # Drawing Player
        player.draw(screen)
        player.update()
        # Calling obstacle group
        obstacle_group.draw(screen)
        obstacle_group.update(speed)
        # Collision detection
        game_active = collision_sprite(player, obstacle_group)

    else:  # "Game Over Screen"
        screen.fill((94, 129, 162))  # dark screen
        screen.blit(player_stand, player_stand_rect)  # display player over dark screen
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)  # Sets max frame rate to 60 while loop is running.

