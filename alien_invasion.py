"""
Final Project: Alien Invasion
Ethan Swearingen
The purpose of this project is to have a ship that can move around and destroy the aliens that come onto the screen
Starter code is from https://github.com/RedBeard41/alien_Invasion_starter , and from the tutorials posted by Proffessor RedBeard
04/19/2026
"""
import sys
import pygame
import time
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from hud import HUD
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        # Initialize pygame and settings
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
        # Load and scale the background image to fit the screen dimensions
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg,
            (self.settings.screen_w, self.settings.screen_h)
        )

        
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.game_active = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.last_wave_time = time.time()
        self.play_button = Button(self, 'Play Game')
        pygame.mouse.set_visible(True)
        

        # Initialize the mixer for sound playback
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.3)

        # Create main game objects
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.fleet.empty()

    def run_game(self):
        """Start the main loop for the game. Handles events, updates, collisions, and rendering."""
        while self.running:
            self.check_events()
            if self.game_active:
                self.ship.update()
                self.ship.arsenal.update_arsenal()
                self.alien_fleet.update_fleet()
                self.check_collisions()
                self._maybe_spawn_wave()
            self.update_screen()
            self.clock.tick(self.settings.FPS)

    def _maybe_spawn_wave(self):
        """Spawn a new wave of aliens if enough time has passed since the last wave."""
        now = time.time()
        if now - self.last_wave_time >= self.settings.wave_spawn_time:
            self.alien_fleet.create_fleet()
            self.game_stats.update_waves()
            self.HUD.update_waves()
            self.last_wave_time = now

    def update_screen(self):
        """Redraw the screen and flip to the new screen."""
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def check_events(self):
        """Check for events such as key presses, releases, mouse clicks, and quitting the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
                self._check_play_button(event.pos)

    def check_keyup_events(self, event):
        """Check for key releases and set the movement flags accordingly."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def check_keydown_events(self, event):
        """Check for key presses and set the movement flags accordingly."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        # Allow the player to quit the game by pressing Q
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
        # Ignore all other keys so the game doesn't end or error
        else:
            pass

    def check_collisions(self):
        """Check for collisions between bullets and aliens, updating scores. Handle ship-alien collisions via lives system."""
        # Bullet-alien collisions
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.game_stats.update(collisions)
            self.HUD.update_scores()
            self.laser_sound.play()
            self.laser_sound.fadeout(250)
        # Ship-alien collisions
        if pygame.sprite.spritecollideany(self.ship, self.alien_fleet.fleet):
            self._ship_hit()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the play button is clicked."""
        if self.play_button.check_clicked(mouse_pos):
            self._start_new_game()

    def _start_new_game(self):
        """Reset state and start a fresh game session."""
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self.HUD.update_waves()
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.ship.center_ship()
        self.alien_fleet.create_fleet()
        self.game_stats.update_waves()
        self.HUD.update_waves()
        self.last_wave_time = time.time()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _ship_hit(self):
        """Handle ship impact by consuming a life and resetting the wave."""
        if self.game_stats.ships_left > 1:
            self.game_stats.ships_left -= 1
            self.ship.arsenal.arsenal.empty()
            self.alien_fleet.fleet.empty()
            self.alien_fleet.create_fleet()
            self.game_stats.reset_waves()
            self.HUD.update_waves()
            self.ship.center_ship()
            self.last_wave_time = time.time()
            time.sleep(0.5)
            return

        self.game_stats.ships_left = 0
        self.game_active = False
        pygame.mouse.set_visible(True)
        self.game_stats.save_scores()
        print("Game Over! You are out of lives.")


if __name__ == '__main__':
    # Create a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()