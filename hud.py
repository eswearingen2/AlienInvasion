"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Proffessor RedBeard
04/19/2026
"""
import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class HUD:
    """Manage on-screen display of score, lives, waves, and high score."""

    def __init__(self, game):
        """Initialize the HUD and render all display elements."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_file, 
            self.settings.HUD_font_size)
        self.padding = 20
        self.update_scores()
        self.setup_life_image()
        self.update_waves()

    def setup_life_image(self):
        """Load and scale the ship image to display as life indicators."""
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(self.life_image, (
            self.settings.ship_w, self.settings.ship_h
            ))
        self.life_rect = self.life_image.get_rect()

    def update_scores(self):
        """Update all score-related display elements."""
        self.update_max_score()
        self.update_score()
        self.update_hi_score()

    def update_score(self):
        """Render the current score text and position it on screen."""
        score_str = f"Score: {self.game_stats.score: ,.0f}"
        self.score_image = self.font.render(score_str, True, 
            self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + self.padding

    def update_max_score(self):
        """Render the max score achieved in the current session and position it on screen."""
        max_score_str = f"Max-Score: {self.game_stats.max_score: ,.0f}"
        self.max_score_image = self.font.render(max_score_str, True, 
            self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding
    
    def update_hi_score(self):
        """Render the all-time high score and position it at the top center of screen."""
        hi_score_str = f"Hi-Score: {self.game_stats.hi_score: ,.0f}"
        self.hi_score_image = self.font.render(hi_score_str, True, 
            self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_waves(self):
        """Render the wave counter and position it in the left area below lives."""
        wave_str = f"Waves: {self.game_stats.waves}"
        self.wave_image = self.font.render(wave_str, True, 
            self.settings.text_color, None)
        self.wave_rect = self.wave_image.get_rect()
        self.wave_rect.left = self.padding
        self.wave_rect.top = self.life_rect.bottom + self.padding

    def draw_lives(self):
        """Draw ship icons in the top-left corner to represent remaining lives."""
        current_x = self.padding
        current_y = self.padding
        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.settings.ship_w + self.padding

    def draw(self):
        """Draw all HUD elements (scores, waves, and lives) to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.wave_image, self.wave_rect)
        self.draw_lives()