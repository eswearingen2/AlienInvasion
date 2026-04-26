"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Proffessor RedBeard
04/19/2026
"""
from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats:
    """Manage game statistics including score, lives, high score, and waves."""

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """Load high score from file, or initialize to 0 if file does not exist."""
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat().st_size > 0:
            try:
                contents = self.path.read_text()
                self.hi_score = json.loads(contents).get('hi_score', 0)
                return
            except (json.JSONDecodeError, OSError):
                pass

        self.hi_score = 0
        self.save_scores()

    def save_scores(self):
        """Save the current high score to the scores file."""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent = 4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'Files not found. {e}')
    
    def reset_stats(self):
        """Reset all game statistics for a new game session."""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.waves = 0

    def update(self, points):
        """Update score, max score, and high score based on alien collisions."""
        #update score
        self._update_score(points)
        #update max score
        self._update_max_score()
        #update high score
        self._update_hi_score()

    def _update_max_score(self):
        """Update the maximum score reached in the current session."""
        if self.score > self.max_score:
            self.max_score = self.score
        #print(f"Max score: {self.max_score}")

    def _update_hi_score(self):
        """Update the all-time high score if current score exceeds it."""
        if self.score > self.hi_score:
            self.hi_score = self.score
        #print(f"hi_ score: {self.hi_score}")
    
    def _update_score(self, collisions):
        """Add points for each alien destroyed, based on alien_points setting."""
        for alien in collisions:
            self.score += self.settings.alien_points
        #print(f"Score: {self.score}")

    def update_waves(self):
        """Increment the wave counter when a new alien fleet is spawned."""
        self.waves += 1

    def reset_waves(self):
        """Reset the wave counter to 1 when the player loses a life."""
        self.waves = 1