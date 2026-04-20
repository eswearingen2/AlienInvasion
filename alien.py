"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Professor RedBeard
04/19/2026
"""
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """Class representing a single alien."""
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initialize the alien, set position, and movement direction."""
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        self._set_initial_position(x, y)
        self._set_direction()

    def _set_initial_position(self, x, y):
        """Set the alien's initial position."""
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _set_direction(self):
        """Determine if the alien flies straight or toward the center and set direction vector."""
        self.straight = random.random() < 0.5  # 50% chance
        if self.straight:
            if self.rect.y == 0:
                self.dir_x = 0
                self.dir_y = 1  # Down
            elif self.rect.y >= self.settings.screen_h - self.settings.alien_h:
                self.dir_x = 0
                self.dir_y = -1  # Up
            elif self.rect.x == 0:
                self.dir_x = 1
                self.dir_y = 0  # Right
            elif self.rect.x >= self.settings.screen_w - self.settings.alien_w:
                self.dir_x = -1
                self.dir_y = 0  # Left
            else:
                self.dir_x = 0
                self.dir_y = 1
        else:
            center_x = self.settings.screen_w / 2
            center_y = self.settings.screen_h / 2
            dx = center_x - self.x
            dy = center_y - self.y
            mag = (dx ** 2 + dy ** 2) ** 0.5
            if mag != 0:
                self.dir_x = dx / mag
                self.dir_y = dy / mag
            else:
                self.dir_x = 0
                self.dir_y = 0

    def update(self):
        """Move the alien in its assigned direction."""
        temp_speed = self.settings.fleet_speed
        self.x += temp_speed * self.dir_x
        self.y += temp_speed * self.dir_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)

    def draw_alien(self):
        """Draw the alien to the screen."""
        self.screen.blit(self.image, self.rect)