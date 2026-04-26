"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Professor RedBeard
04/19/2026
"""
import pygame
from typing import TYPE_CHECKING
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """Class representing the fleet of aliens."""
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the fleet and create the first wave of aliens."""
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.create_fleet()

    def create_fleet(self):
        """Spawn aliens along all four walls of the screen."""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h
        # Top wall
        for x in range(0, screen_w, alien_w * 2):
            self._create_alien(x, 0)
        # Bottom wall
        for x in range(0, screen_w, alien_w * 2):
            self._create_alien(x, screen_h - alien_h)
        # Left wall
        for y in range(alien_h * 2, screen_h - alien_h * 2, alien_h * 2):
            self._create_alien(0, y)
        # Right wall
        for y in range(alien_h * 2, screen_h - alien_h * 2, alien_h * 2):
            self._create_alien(screen_w - alien_w, y)

    def _create_alien(self, current_x: int, current_y: int):
        """Create a single alien and add it to the fleet."""
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def update_fleet(self):
        """Update all aliens in the fleet."""
        self.fleet.update()

    def draw(self):
        """Draw all aliens in the fleet to the screen."""
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """Check for collisions between the fleet and another group (e.g., bullets)."""
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
