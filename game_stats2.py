class GameStats():
    """Track statistics for the game"""

    def __init__(self,game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False
        with open("highscore.txt","r") as hs:
            high_score = hs.readline()

        self.high_score = int(high_score)


    def reset_stats(self):
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level= 1
