class Settings:
    """Class to store all settings for Alcohol Crusher"""

    def __init__(self):
        """Initialize game's static settings"""
        #Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (249, 247, 248)

        #Fist settings
        self.fist_limit = 1

        #Bullet settings
        self.bullet_width = 5
        self.bullet_height = 5
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 6

        #Alcohol setings
        self.pack_drop_speed = 10
        
        #How quickly game speeds up
        self.speedup_scale = 1.2
        #How quickly alcohol point values increase
        self.score_scale = 2.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change during the crush."""
        self.fist_speed = 3.5
        self.bullet_speed = 4.5
        self.beer_speed = 2.5
        #pack_direction of 1 represents right; -1 left.
        self.pack_direction = 1 
        #Scoring settings
        self.beer_points = 5000

    def increase_speed(self):
        """Increase speed settings and alcohol point values."""
        self.fist_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.beer_speed *= self.speedup_scale
        self.beer_points = int(self.beer_points * self.score_scale)
