import json

class HighScores:
    """Class for High Scores."""
    
    def __init__(self, filename='high_scores.json'):
        """Initialize High Scores."""
        self.filename = filename
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """Load High Scores from file."""
        try:
            with open(self.filename, 'r') as f:
                high_scores = json.load(f)
        except FileNotFoundError:
            high_scores = []
        finally:
            return high_scores

    def save_high_scores(self):
        """Save High Scores to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.high_scores, f)

    def add_score(self, nickname, score):
        """Add a new score to High Scores list if it's a top ten score."""
        self.high_scores.append({'nickname': nickname, 'score': score})
        self.high_scores.sort(key=lambda s: s['score'], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_high_scores()

    def get_high_scores(self):
        """Return High Scores list."""
        return self.high_scores
