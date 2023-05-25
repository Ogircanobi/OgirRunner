# Rigoberto Alvarez
# First pygame project
# Completed following youTube tutorial: https://www.youtube.com/watch?v=AY9MnQ4x3zk

import pygame
from sys import exit
from random import randint, choice


# Creating sprite class for Player. Sprite groups draw sprites and also Update sprites.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Initializing sprite class within class
        # minimum two attributes required image and rectangle
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]  # list holds player_walk_1 and player_walk_2 surfaces
        self.player_index = 0  # Use as index to pick either player_walk_1 or player_walk_2 from player_walk list
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()  # surface to dislpay when jumping

        self.image = self.player_walk[self.player_index] # gives you index 0
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

        # Function defining player input
    def player_input(self):
        keys = pygame.key.get_pressed() # retrive list of all possible key inputs
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  # if space bar is being pressed then...
            self.gravity = -20 # ...jump player
            self.jump_sound.play()

    def apply_gravity(self): # appling gravity
        self.gravity += 1
        self.rect.y += self.gravity  # picking rectangle to move it and applying gravity.
        if self.rect.bottom >= 300:  # make sure player stops at the ground.
            self.rect.bottom = 300

    # Method for controlling animation frames
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    # Defining an update method. Instead of calling each method individually, call the update method.
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# Creating sprite class for obstacles
class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type): # use second argument to identify what type of enemy you want
        super().__init__()
        # before creating image, check if type is fly or snail
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210 # y position needed for fly and snail since they are at different heights
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0 # index to track animations
        self.image = self.frames[self.animation_index]  # list of differnt image frames
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    # this method delets sprites that go too far left ( off the screen)
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Function that displays score on screen
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time  # gets current time and saves it as current_time variable. Subtracts start time when you die and restart.
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))  # new surface for score
    score_rect = score_surf.get_rect(center=(400, 50))  # rectangle for score_surf
    screen.blit(score_surf, score_rect)  # Draw out on screen
    return current_time


# function that moves obstacles from obstacle_list
def obstacle_movement(obstacle_list):
    if obstacle_list:  # Make sure list is not empty
        for obstacle_rect in obstacle_list: # loop that moves every object in list by iterating through it.
            obstacle_rect.x -= 5  # Distance movement
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)  # place obstacle on screen
            else:
                screen.blit(fly_surf, obstacle_rect)  # place obstacle on screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]  # list comprehension that removes any items that have passed the left side of screen
        return obstacle_list
    else:
        return []  # if list is empty return empty list


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300: # if player is not touching floor show jump image
        player_surf = player_jump
    else: # walking animation
        player_index += 0.1 # increase walk index by small increments
        if player_index >= len(player_walk): # loop index back to 0
            player_index = 0
        player_surf = player_walk[int(player_index)] # changing between walking animations

    # play walking animation if the player is on floor
    # display the jump surface when player is not on floor

# Create window using .init()
# This starts pygame and initiates all necessary functions
pygame.init()
# Provide Display Surface (The window player sees).
# set_mode needs at least one argument (tuple)
# that represents with, height.
screen = pygame.display.set_mode((800, 400))
# set title of game
pygame.display.set_caption('Rigo Runner')
# create clock object to control frame rate
clock = pygame.time.Clock()
# create a font using .Font(font type, font size) using fonts from font folder
test_font = pygame.font.Font('font/Pixeltype.ttf',50) # 'None' = default font.
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1) # -1 loops music forever

# Groups: collections of sprites
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Creating new surfaces, which are objects that appear over display surface.
# We can create an image or in this case load an image.
sky_surface = pygame.image.load('graphics/Sky.png').convert() #.convert() converts image to an easier to use image (game runs faster)
ground_surface = pygame.image.load('graphics/ground.png').convert()
# Creating text surface using .render(text, Anti Aliasing(smooth text) , color)
# This will display test on surface.
# score_surf = test_font.render('My game', False, (64, 64, 64))
# score_rect = score_surf.get_rect(center = (400, 50))

# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]


# fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]  # list holds player_walk_1 and player_walk_2 surfaces
player_index = 0  # Use as index to pick either player_walk_1 or player_walk_2 from player_walk list
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()  # surface to dislpay when jumping

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))  # .get_rect() takes surface and creates identical sized rectangle
player_gravity = 0

# Intro screen
final_score = 0
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()  #importing image
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # scaleing image with rotozoom
player_stand_rect = player_stand.get_rect(center=(400,200)) # Create rectangle

game_name = test_font.render('RigoRunner', False, (111,196,169))
game_name_rect = game_name.get_rect(center= (400,80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400, 340))


# Timer
obstacle_timer = pygame.USEREVENT + 1 # always include + 1 when creating a custom user event (see documentation)
pygame.time.set_timer(obstacle_timer, 1500) # trigger customer event above at certain intervals

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

##############################################################################################
# display surface closes unless a while True loop is created:
# entire game runs inside while true loop
while True:
    #EVENT LOOP that checks for all possible types of player input using .event.get()
    for event in pygame.event.get():
        # First item in loop is an event to detect player closing the window.
        # .QUIT is a constant synonymous with pressing x button of window
        if event.type == pygame.QUIT:
            pygame.quit()# essentially the opposite of .init()
            exit()# exit method from sys cancels all code running

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: # Jumps player by clicking with mouse
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:  # jumps player by pressing spacebar
                   player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == snail_animation_timer: # if statement that animates snail based on timer
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer: # if statement that animates fly based on its timer
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        # Draw all our elements. Pygame draws in order of code entered
        # We use screen.blit(surface,(position)
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)  # Drawing rectangle around text
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # snail_rect.x -= 8
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        # Calling obstacle group
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)


    else:  # "Game Over Screen"
        screen.fill((94, 129, 162))  # dark screen
        screen.blit(player_stand, player_stand_rect)  # display player over dark screen
        obstacle_rect_list.clear()  # clear obstacle_rect list
        player_rect.midbottom = (80,300)  # Reset player to ground if died while jumping
        player_gravity = 0  # reset gravity
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)


    # Using the key.get_pressed() method returns a dictionary
    # with all the keys currently being pressed
    # Use documentation to find name for each key. Use if statement to
    # check the keys dictionary
    # to see if that key is being pressed
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:
    #    print('jump')
    # Check if player_rect is colliding with snail_rect
    # this method returns true or false
    #if player_rect.colliderect(snail_rect):
    #    print('collision')
    #mouse_pos = pygame.mouse.get_pos()
    #if player_rect.collidepoint((mouse_pos)):
    #    print(pygame.mouse.get_pressed())
    # .display.update() updates display with any changes made
    pygame.display.update()
    clock.tick(60)  # Sets max frame rate to 60 while loop is running.

