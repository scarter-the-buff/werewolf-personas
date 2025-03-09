import json

class GameManager:
    def __init__(self):
        self.count = 0  # Initialize the count

    def makeGame(self):
        self.count += 1

        game = {
            "game_id": self.count,
            "players": [],
            "player_ids": [],
            "transcript": [],
            "turn": 0,
            "winning_team": 0,
        }
        
    
        with open("games.json", "w") as json_file:
            json.dump(game, json_file, indent=4)  # `indent=4` makes it pretty-printed