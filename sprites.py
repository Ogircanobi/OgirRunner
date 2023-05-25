# Rigoberto Alvarez
# sprites.py file: contains class definitions for all sprites in game.

import pygame
from random import randint


# Creating sprite class for Player. Sprite groups draw sprites and also Update sprites.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initializing sprite class within class
        # minimum two attributes required image and rectangle
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]  # list holds player_walk_1 and player_walk_2 surfaces
        self.player_index = 0  # Use as index to pick either player_walk_1 or player_walk_2 from player_walk list
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()  # Jump image

        self.image = self.player_walk[self.player_index]  # gives you index 0
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

        # Function defining player input
    def player_input(self):
        keys = pygame.key.get_pressed()  # retrieve list of all possible key inputs
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  # if space bar is being pressed then...
            self.gravity = -20  # ...jump player
            self.jump_sound.play()

    def apply_gravity(self):  # applying gravity
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
        # before creating image, check if type is fly or snail
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210  # y position needed for fly and snail since they are at different heights
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0  # index to track animations
        self.image = self.frames[self.animation_index]  # list of differnt image frames
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()

    # this method deletes sprites that go too far left ( off the screen)
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
