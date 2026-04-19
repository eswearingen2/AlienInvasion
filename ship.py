"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Professor RedBeard
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

        # Load the ship image once and keep the original for rotation
        loaded_image = pygame.image.load(self.settings.ship_file)
        self.original_image = pygame.transform.scale(loaded_image, 
            (self.settings.ship_w, self.settings.ship_h)
        )
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # Set the ship's starting position to the center of the screen
        self.rect.center = self.screen.get_rect().center
        
        # Set the current angle of the ship to 0 so that it starts facing up
        self.current_angle = 0 

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Store a decimal value for the ship's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.arsenal = arsenal

    def update(self):
        # Updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        angle = 0
        # Adding this to make a boundary for the ship to not go off the screen and to rotate the ship in the direction it is moving
        # Also replaced the if statements with elif statements so that the ship can only move in one direction at a time
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
            self.current_angle = -90
        elif self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
            self.current_angle = 90
        elif self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
            self.current_angle = 0
        elif self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
            self.current_angle = 180

        # Rotate the ship image based on the current angle using the original image
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
    
        # After rotating the image, we need to update the rect to match the new image size and keep the center of the ship consistent
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Update the ship's rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        # Drawing the ship and the bullets to the screen
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
    
    def fire(self):
        # Fire a bullet if the limit has not been reached yet, and play the laser sound effect
        return self.arsenal.fire_bullet()
    