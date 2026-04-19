"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Proffessor RedBeard
04/19/2026
"""
import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal: 
    def __init__(self, game: 'AlienInvasion'):
        # Initialize the arsenal
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        # Update the position of the bullets and get rid of old bullets
        self.arsenal.update()
        self.remove_bullets_offscreen()

    def remove_bullets_offscreen(self):
        # Remove bullets that have disappeared off the top of the screen
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        # Draw the bullets to the screen
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        # Fire a bullet if the limit has not been reached yet, and play the laser sound effect
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False