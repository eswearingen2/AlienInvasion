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
        """Initialize the arsenal with an empty bullet group."""
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """Update the position of all bullets and remove off-screen bullets."""
        self.arsenal.update()
        self.remove_bullets_offscreen()

    def remove_bullets_offscreen(self):
        """Remove bullets that have moved off any edge of the screen."""
        screen_rect = self.game.screen.get_rect()
        for bullet in self.arsenal.copy():
            if (bullet.rect.bottom <= 0 or
                bullet.rect.top >= screen_rect.height or
                bullet.rect.right <= 0 or
                bullet.rect.left >= screen_rect.width):
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw all active bullets to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        """Create and add a new bullet if the bullet limit has not been reached."""
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False