import pygame.font

class TextInput:
    """Class for the input of text."""

    def __init__(self, ac_game, prompt):
        """Initialize text input attributes."""
        self.screen = ac_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ac_game.settings

        # Font settings, None works
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial text image
        self.text = ""
        self.prompt = prompt
        self._prep_text_image()

    def _prep_text_image(self):
        """Turn the text into a rendered image and center text on button."""
        full_text = f"{self.prompt} {self.text}"
        self.text_image = self.font.render(full_text, True, self.text_color, self.settings.bg_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.screen_rect.center

    def draw_text(self):
        """Draw the text to screen."""
        self.text_image_rect.centerx = self.screen_rect.centerx
        self.text_image_rect.centery = self.screen_rect.centery - 30
        self.screen.blit(self.text_image, self.text_image_rect)

    def update_text(self, event):
        """Update the text based on keys typed."""
        if event.unicode.isalpha() and len(self.text) < 3:
            # Add letter to the text
            self.text += event.unicode
        elif event.key == pygame.K_BACKSPACE:
            # Remove the last letter
            self.text = self.text[:-1]
        self._prep_text_image()
