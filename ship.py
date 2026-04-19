"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Proffessor RedBeard
04/19/2026
"""
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal



class Ship: 
    
    
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        # Initialize the ship
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        # Load the ship image and get its rect and starting position
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        self.rect = self.image.get_rect()
        self.rect.center = self.boundaries.center

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.x = float(self.rect.x)
        self.arsenal = arsenal

    def update(self):
        # Updating the posistion of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        # Adding this to make a boundary for the ship to not go off the screen
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.rect.y -= temp_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.rect.y += temp_speed

        self.rect.x = self.x

    def draw(self):
        # Drawing the ship and the bullets to the screen
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
    
    def fire(self):
        # Fire a bullet if the limit has not been reached yet, and play the laser sound effect
        return self.arsenal.fire_bullet()
    