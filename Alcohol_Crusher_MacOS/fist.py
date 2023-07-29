import pygame

class Fist:
    """Class for fist."""

    def __init__(self, ac_game):
        """Initialize fist and set its starting position."""
        self.screen = ac_game.screen
        self.settings = ac_game.settings
        self.screen_rect = ac_game.screen.get_rect()

        # Load fist image and get its rect.
        self.image = pygame.image.load('fist_bgver4.bmp')
        self.small_image = pygame.image.load('fist_small.bmp')  
        self.rect = self.image.get_rect()

        # Start each new fist at the bottom center of screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the fists exact horizontal position.
        self.x = float(self.rect.x)

        #Movement flags; start with fist thats not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update position of fist based on the movement flags."""
        #Update fists x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.fist_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.fist_speed

        #Update rect object from self.x
        self.rect.x = self.x

    def center_fist(self):
        """Center fist on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw fist at its current location"""
        self.screen.blit(self.image, self.rect)