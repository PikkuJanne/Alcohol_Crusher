import pygame.font

class Nappi:
    """Class to build buttons for the crush."""

    def __init__(self, ac_game, msg):
        """Initialize button attributes."""
        self.screen = ac_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set dimensions and properties of button.
        self.width, self.height = 450, 113
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helvetica', 72)

        #Build buttons rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y = self.screen_rect.centery - 350
        #The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_nappi(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class HighScoreButton:
    """Class to build a High Score button for the crush."""

    def __init__(self, ac_game, msg):
        """Initialize button attributes."""
        self.screen = ac_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 450, 113
        self.button_color = (255, 0, 0)  
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helvetica', 72)

        # Build the button's rect object and place it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery - 200 # position under the Crush button

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class AboutButton:
    """Class to build an about button for the crush."""

    def __init__(self, ac_game, msg):
        """Initialize button attributes."""
        self.screen = ac_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 450, 113
        self.button_color = (255, 0, 0) 
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helvetica', 72)

        # Build the button's rect object and place it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery - 50 # position under the HighScoreButton

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class QuitButton:
    """Class to build a quit button for the crush."""

    def __init__(self, ac_game, msg):
        """Initialize button attributes."""
        self.screen = ac_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 450, 113
        self.button_color = (255, 0, 0)  
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helvetica', 72)

        # Build the button's rect object and place it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery + 100  # position under the AboutButton

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class BackButton:
    """Class to build a back button for the crush."""

    def __init__(self, ac_game, msg):
        """Initialize button attributes."""
        self.screen = ac_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 400, 100
        self.button_color = (255, 0, 0)  
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helvetica', 60)

        # Build the button's rect object and place it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = 20
        self.rect.top = 20

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)






    

