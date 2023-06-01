# Rigoberto Alvarez
# sprites.py file: contains class definitions for all sprites in game.

import pygame
from random import randint


# Creating sprite class for Player. Sprite groups draw sprites and also Update sprites.
class Player(pygame.sprite.Sprite):
    def __init__(self): # constructor method
        super().__init__()  # Initializing sprite class within class
        # minimum two attributes required image and rectangle
        player_walk_1 = pygame.image.load('graphics/Player/Martian/1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/Martian/2.png').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/Player/Martian/3.png').convert_alpha()
        player_walk_4 = pygame.image.load('graphics/Player/Martian/4.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4]  # list holds animation surfaces
        self.player_index = 0  # Use as index to pick either player_walk_1 or player_walk_2 from player_walk list
        self.player_jump = pygame.image.load('graphics/Player/Martian/2.png').convert_alpha()  # Jump image
        self.floor = 275 # This variable adjust level of floor for all functions that use it.
        self.image = self.player_walk[self.player_index]  # gives you index 0
        self.rect = self.image.get_rect(midbottom=(80, self.floor))  # this line creates collision rect.
        self.rect.inflate_ip(-self.rect.width // 4, -self.rect.height // 4) # adjusts rectangle size
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)


        # Function defining player input
    def player_input(self):
        keys = pygame.key.get_pressed()  # retrieve list of all possible key inputs
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.floor:  # if space bar is being pressed then...
            self.gravity = -20  # ...jump player
            self.jump_sound.play()

    def apply_gravity(self):  # applying gravity
        self.gravity += 1
        self.rect.y += self.gravity  # picking rectangle to move it and applying gravity.
        if self.rect.bottom >= self.floor:  # make sure player stops at the ground.
            self.rect.bottom = self.floor

    # Method for controlling animation frames
    def animation_state(self):
        if self.rect.bottom < self.floor:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    # Defining an update method. Instead of calling each method individually, call the update method.
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# Creating sprite class for obstacles
class Obstacle(pygame.sprite.Sprite):

    def __init__(self,type):  # use second argument to identify what type of enemy you want
        super().__init__()
        # before creating image, check if type is fly or ground enemy
        if type == 'fly':  # load flying images /
            fly_1 = pygame.image.load('graphics/UFO/GreenUFO.png')
            fly_1 = pygame.transform.scale(fly_1, (80, 40))  # scaling picture to 80 x 40 size
            fly_1 = fly_1.convert()
            fly_2 = pygame.image.load('graphics/UFO/blueUFO.png')
            fly_2 = pygame.transform.scale(fly_2, (80, 40))  # scaling picture to 80 x 40 size
            fly_2 = fly_2.convert()
            fly_3 = pygame.image.load('graphics/UFO/yellowUFO.png')
            fly_3 = pygame.transform.scale(fly_3, (80, 40))  # scaling picture to 80 x 40 size
            fly_3 = fly_3.convert()

            self.frames = [fly_1, fly_2, fly_3]
            y_pos = 200  # y position needed for fly and snail since they are at different heights
        else:
            walking_1 = pygame.image.load('graphics/Slime/slimeWalk1.png').convert_alpha()
            walking_2 = pygame.image.load('graphics/Slime/slimeWalk2.png').convert_alpha()
            self.frames = [walking_1, walking_2]
            y_pos = 300

        self.animation_index = 0  # index to track animations
        self.image = self.frames[self.animation_index]  # list of different image frames
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        self.rect.inflate_ip(-self.rect.width // 8, -self.rect.height // 8)  # making rectangle smaller

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # moves sprite based on speed (from speed_update() function)
    def update(self, speed):
        self.animation_state()
        self.rect.x -= speed
        self.destroy()

    # this method deletes sprites that go too far left ( off the screen)
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
