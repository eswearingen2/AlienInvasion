"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Professor RedBeard
04/19/2026
"""

"""
Ship class for Alien Invasion game.
Handles ship movement, drawing, firing, and collision logic.
"""
import pygame
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship(pygame.sprite.Sprite):
    """Class representing the player's ship."""
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        loaded_image = pygame.image.load(self.settings.ship_file)
        self.original_image = pygame.transform.scale(loaded_image, 
            (self.settings.ship_w, self.settings.ship_h)
        )
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.current_angle = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.arsenal = arsenal

    def update(self):
        """Update the ship's position and arsenal."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Update the ship's position based on movement flags and handle rotation."""
        temp_speed = self.settings.ship_speed
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
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        """Draw the ship and its bullets to the screen."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
    
    def fire(self):
        """Fire a bullet if the limit has not been reached yet."""
        return self.arsenal.fire_bullet()
    
    def center_ship(self):
        """Center the ship on the screen and reset its position values."""
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
