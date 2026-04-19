"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Proffessor RedBeard
04/19/2026
"""
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    def __init__(self, game: 'AlienInvasion'):
        # Initialize the bullet and set its starting position
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings
        self.angle = game.ship.current_angle

        # Load the bullet image
        self.image = pygame.image.load(self.settings.bullet_file)

        # Rotate the bullet image based on the ship's current angle
        if self.angle in [0, 180]:  # Facing up or down
            self.image = pygame.transform.rotate(self.image, self.angle)
        else:  # Facing left or right
            self.image = pygame.transform.rotate(self.image, self.angle)
     
        # Get the rect of the bullet based on the rotated image
        self.rect = self.image.get_rect()
        
        # Set the rect's center to match the ship's corresponding spawn point for correct alignment
        if self.angle == 0:    # Up - spawn from top center
            self.rect.center = game.ship.rect.midtop
        elif self.angle == 180: # Down - spawn from bottom center
            self.rect.center = game.ship.rect.midbottom
        elif self.angle == -90: # Right - spawn from right center
            self.rect.center = game.ship.rect.midright
        elif self.angle == 90:  # Left - spawn from left center
            self.rect.center = game.ship.rect.midleft

        # Store the bullet's position as a decimal value for more precise movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        # Move the bullet up the screen
        if self.angle == 0:    # Up
            self.y -= self.settings.bullet_speed
        elif self.angle == 180: # Down
            self.y += self.settings.bullet_speed
        elif self.angle == -90: # Right
            self.x += self.settings.bullet_speed
        elif self.angle == 90:  # Left
             self.x -= self.settings.bullet_speed

        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        # Draw the bullet to the screen
        self.screen.blit(self.image, self.rect)