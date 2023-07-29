class GameStats:
    """Track stats for Alcohol Crusher."""

    def __init__(self, ac_game, high_scores):
        """Initialize stats."""
        self.settings = ac_game.settings
        self.high_scores = high_scores
        self.reset_stats()

    def reset_stats(self):
        """Initialize stats that can change during the crush."""
        self.fists_left = self.settings.fist_limit
        self.score = 0
        self.level = 1
        if self.high_scores.get_high_scores():
            self.high_score = self.high_scores.get_high_scores()[0]['score']
        else:
            self.high_score = 0

        
