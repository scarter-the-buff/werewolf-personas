# Define crew object
class Crew():
    def __init__(self, player_list):
        self.players = player_list

    def __repr__(self):
        players = [player.name for player in self.players]
        return " ".join(players)