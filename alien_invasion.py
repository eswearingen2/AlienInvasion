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


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
        pygame.display.set_caption(self.settings.name)

        # Load and scale the background image to fit the screen dimensions
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg,
            (self.settings.screen_w, self.settings.screen_h)
        )

        self.running = True
        self.clock = pygame.time.Clock()
        self.last_wave_time = time.time()

        # Initialize the mixer for sound playback
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.3)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            self.check_events()
            self.ship.update()
            self.ship.arsenal.update_arsenal()
            self.alien_fleet.update_fleet()
            self.check_collisions()
            self._maybe_spawn_wave()
            self.update_screen()
            self.clock.tick(self.settings.FPS)

    def _maybe_spawn_wave(self):
        now = time.time()
        if now - self.last_wave_time >= self.settings.wave_spawn_time:
            self.alien_fleet.create_fleet()
            self.last_wave_time = now

    def update_screen(self):
        """Redraw the screen and flip to the new screen."""
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        pygame.display.flip()

    def check_events(self):
        """Check for events such as key presses and releases, and quitting the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

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
            pygame.quit()
            sys.exit()
        # Ignore all other keys so the game doesn't end or error
        else:
            pass

    def check_collisions(self):
        """Check for collisions between bullets and aliens."""
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.laser_sound.play()
            self.laser_sound.fadeout(250)


if __name__ == '__main__':
    # Create a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()