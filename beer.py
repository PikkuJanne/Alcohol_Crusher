import pygame
from pygame.sprite import Sprite

class Beer(Sprite):
    """A class for an single alcohol in the pack."""

    def __init__(self, ac_game, image_path):
        """Initialize alcohol and set its starting position."""
        super().__init__()
        self.screen = ac_game.screen
        self.settings = ac_game.settings

        # Load the beer image and set its rect attribute.
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        #Start each new beer near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the beer's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alcohol is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move alcohol right or left."""
        self.x += self.settings.beer_speed * self.settings.pack_direction
        self.rect.x = self.x