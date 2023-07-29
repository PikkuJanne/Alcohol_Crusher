import sys
import random
from time import sleep
import pygame
from alcohol_settings import Settings
from alcohol_stats import GameStats
from scoreboard import Scoreboard
from nappi import Nappi
from fist import Fist
from alcohol_bullet import Bullet
from beer import Beer
from high_scores import HighScores
from text_input import TextInput
from nappi import HighScoreButton
from nappi import BackButton
import pygame_textinput
from nappi import AboutButton
from nappi import QuitButton

class AlcoholCrusher:
    """Main class to manage alcohol assets and behavior."""

    def __init__(self):
        """Initialize the crush and create alcohol resources."""
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alcohol Crusher")

        self.screen_rect = self.screen.get_rect()

        #Create instance to store crush statistics and create scoreboard.
        self.high_scores = HighScores()
        self.stats = GameStats(self, self.high_scores)
        self.sb = Scoreboard(self)

        self.fist = Fist(self)
        self.bullets = pygame.sprite.Group()
        self.beers = pygame.sprite.Group()

        # List of images for different levels.
        self.beer_images = ['beerfinalver5.bmp', 'winefinalver4.bmp', 'spiritsfinalver4.bmp']
        # Randomly select an image for the first level.
        self.current_beer_image = random.choice(self.beer_images)

        self._create_pack()

        #Start Alcohol Crusher inactive.
        self.game_active = False
        self.game_paused = False
        self.sounds_on = False
        self.about_screen_active = False

        #Make Crush button.
        self.crush_button = Nappi(self, "Crush")

        self.text_input = TextInput(self, "Give your Scene nick:")

        self.high_score_button = HighScoreButton(self, "High Scores")
        self.high_scores_screen_active = False

        self.about_button = AboutButton(self, "About")
        self.quit_button = QuitButton(self, "Quit")
        self.back_button = BackButton(self, "Back")

        self.font = pygame.font.Font(None, 60)
        self.text_color = (0, 0, 0) 

        self.shoot_sound = pygame.mixer.Sound('cannonfire_01.wav')
        self.fist_destroyed_sound = pygame.mixer.Sound('crowdreaction_negative_01.wav')
        self.enemy_destroyed_sound = pygame.mixer.Sound('glassbreak_01.wav')

    def run_game(self):
        """Start main loop for the crush"""
        while True:
            self._check_events()
            if self.about_screen_active:
                self._update_about_screen()
            elif self.game_active and not self.game_paused:
                self.fist.update()
                self._update_bullets()
                self._update_beers()
            if not self.about_screen_active:
                self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_active:
                    self.text_input.update_text(event)
                elif event.key == pygame.K_p:
                        if self.game_active:
                            self.game_paused = not self.game_paused
                elif event.key == pygame.K_s:
                    self.sounds_on = not self.sounds_on
                else:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_crush_button(mouse_pos)
                self._check_high_score_button(mouse_pos)
                self._check_back_button(mouse_pos)
                self._check_about_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_crush_button(self, mouse_pos):
        """Start new game when player clicks Crush."""
        nappi_clicked = self.crush_button.rect.collidepoint(mouse_pos)
        if nappi_clicked and not self.game_active:
            #Reset crush settings.
            self.settings.initialize_dynamic_settings()
            #Reset crush stats.
            self.stats.reset_stats()
            self.sb.prep_high_score()
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True
            #Get rid of remaining bullets and beers.
            self.bullets.empty()
            self.beers.empty()
            #Create new pack and center fist.
            self._create_pack()
            self.fist.center_fist()
            #Hide mouse cursor
            pygame.mouse.set_visible(False)
        if not self.game_active:
            # If crush is over, add score to the high scores
            if self.text_input.text:  # check if text is not empty
                self.high_scores.add_score(self.text_input.text, self.stats.score)

    def _check_high_score_button(self, mouse_pos):
        """Show high score screen when player clicks High Score."""
        button_clicked = self.high_score_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.high_scores_screen_active = True
            self._update_high_scores_screen()

    def _check_about_button(self, mouse_pos):
        """Show about screen when player clicks About."""
        button_clicked = self.about_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.about_screen_active = True

    def _check_quit_button(self, mouse_pos):
        """Quit game when player clicks Quit."""
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            sys.exit()

    def _check_back_button(self, mouse_pos):
        """Go back to main screen when player clicks Back."""
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.high_scores_screen_active:
            self.high_scores_screen_active = False
        elif button_clicked and self.about_screen_active:
            self.about_screen_active = False

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.fist.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.fist.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.fist.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.fist.moving_left = False

    def _fire_bullet(self):
        """Create new bullet and add it to bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            if self.sounds_on:
                self.shoot_sound.play()
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions.
        self.bullets.update()
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_beer_collisions()
        
    def _check_bullet_beer_collisions(self):
        """Respond to bullet-alcohol collisions."""
        #Remove any bullets and alcohols that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.beers, True, True)
        if collisions:
            for beers in collisions.values():
                if self.sounds_on:
                    self.enemy_destroyed_sound.play()
                self.stats.score += self.settings.beer_points * len(beers)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.beers:
            #Destroy existing bullets and create new pack.
            self.bullets.empty()
            self._create_pack()
            self.settings.increase_speed()
            # Randomly select an image for the next level.
            self.current_beer_image = random.choice(self.beer_images)
            #Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _check_beers_bottom(self):
        """Check if any alcohols have reached bottom of the screen."""
        for beer in self.beers.sprites():
            if beer.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the fist got hit.
                self._fist_hit()
                break

    def _get_nickname(self):
        """Show textbox on the screen and get player's Scene nickname."""
        manager = pygame_textinput.TextInputManager()
        text_input = pygame_textinput.TextInputVisualizer(manager=manager)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            text_input.update(events)

            if pygame.K_RETURN in [event.key for event in events if event.type == pygame.KEYDOWN]:
                return manager.value

            self.screen.fill(self.settings.bg_color)
            self.text_input.draw_text()  # Draw the text input prompt
            self.screen.blit(text_input.surface, (self.screen.get_rect().centerx, self.screen.get_rect().centery))
            pygame.display.update()

    def _fist_hit(self):
        """Respond to fist being hit by alcohol."""
        if self.stats.fists_left > 0:
            #Decrement beers_left.
            self.stats.fists_left -= 1
            #Get rid of any remaining bullets and alcohols.
            self.bullets.empty()
            self.beers.empty()
            #Create a new pack and center fist.
            self._create_pack()
            if self.sounds_on:
                self.fist_destroyed_sound.play()
            self.fist.center_fist()
            #Pause.
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

            # Draw the text input prompt
            self.text_input.draw_text()
            pygame.display.flip()  # Update the screen

            # Ask for player's Scene nickname and add their score to the high score list
            nickname = self._get_nickname()
            self.high_scores.add_score(nickname, self.stats.score)

    def _update_beers(self):
        """Check if the pack is at an edge, then update positions."""
        self._check_pack_edges()
        self.beers.update()
        #Look for alcohol-fist collisions.
        if pygame.sprite.spritecollideany(self.fist, self.beers):
            self._fist_hit()
        #Look for alcohols hitting the bottom of the screen.
        self._check_beers_bottom()

    def _create_pack(self):
        """Create pack of alcohol."""
        # Create an alcohol and keep adding alcohols until theres no room left.
        # Spacing between alcohols is less than one alcohol width and one alcohol height.
        beer = Beer(self, self.current_beer_image)
        beer_width, beer_height = beer.rect.size

        current_x, current_y = beer_width, beer_height
        while current_y < (self.settings.screen_height - 5 * beer_height):
            while current_x < (self.settings.screen_width - 2 * beer_width):
                self._create_beer(current_x, current_y)
                current_x += 1.20 * beer_width
            
            #Finished a row; reset x value and increment y value.
            current_x = beer_width
            current_y += 1.3 * beer_height

    def _create_beer(self, x_position, y_position):
        """Create alcohol and lace it in the row."""
        new_beer = Beer(self, self.current_beer_image)
        new_beer.x = x_position
        new_beer.rect.x = x_position
        new_beer.rect.y = y_position
        self.beers.add(new_beer)

    def _check_pack_edges(self):
        """Respond appropriately if any alcohols have reached an edge."""
        for beer in self.beers.sprites():
            if beer.check_edges():
                self._change_pack_direction()
                break

    def _change_pack_direction(self):
        """Drop the entire pack and change the pack's direction."""
        for beer in self.beers.sprites():
            beer.rect.y += self.settings.pack_drop_speed
        self.settings.pack_direction *= -1

    def _update_high_scores_screen(self):
        """Update high scores screen."""
        self.screen.fill(self.settings.bg_color)
        self._display_high_scores()
        self.back_button.draw_button()
        pygame.display.flip()

    def _update_about_screen(self):
        """Update about screen."""
        self.screen.fill(self.settings.bg_color)
        self._display_about_text()
        self.back_button.draw_button()
        pygame.display.flip()

    def _display_high_scores(self):
        """Display High Score list."""
        high_scores = self.high_scores.get_high_scores()
        for index, score_dict in enumerate(high_scores):
            score_str = f"{index + 1}. {score_dict['nickname']}: {score_dict['score']}"
            score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
            score_rect = score_image.get_rect()
            score_rect.centerx = self.screen.get_rect().centerx  
            score_rect.top = self.screen.get_rect().top + 200 + (index * score_rect.height) + (index * 15)
            self.screen.blit(score_image, score_rect)

    def _display_about_text(self):
        """Display about text."""
        about_text = (
            "\n\n\nWelcome to the world's first and only Straight Edge shoot 'em up ALCOHOL CRUSHER!\n"
            "Crush all beer, wine and spirits that cross your path on your quest to rid this world of alcohol.\n\n"
            "CONTROLS:\n"
            "arrow left      move Straight Edge fist left\n"
            "arrow right    move Straight Edge fist right\n"
            "space             shoot bullets\n"
            "p                     pause game\n"
            "s                     sound effects on/off\n"
            "q                     quit game\n\n"
            "CREDITS:\n"
            "Game by        Janne Vuorela\n"
            "Sound FX       Zach\n"
            "Graphics       Adobe Ai\n"
            "License         Creative Commons"
        )
        about_text = about_text.replace('\t', '    ')  
        about_text_lines = about_text.split('\n')
        for index, line in enumerate(about_text_lines):
            line_image = self.font.render(line, True, self.text_color, self.settings.bg_color)
            line_rect = line_image.get_rect()
            line_rect.left = self.screen_rect.left + 20
            line_rect.top = self.screen_rect.top + (index * line_rect.height) + (index * 15)
            self.screen.blit(line_image, line_rect)

    def _update_screen(self):
        """Update images on screen and flip to new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.fist.blitme()
        self.beers.draw(self.screen)

        # Draw score info.
        self.sb.show_score()

        # Draw buttons if the game is inactive.
        if not self.game_active:
            if self.high_scores_screen_active:
                self._update_high_scores_screen()
            else:
                self.text_input.draw_text()
                self.crush_button.draw_nappi()  
                self.high_score_button.draw_button()
                self.about_button.draw_button()
                self.quit_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a crush instance and run the game.
    ac = AlcoholCrusher()
    ac.run_game()