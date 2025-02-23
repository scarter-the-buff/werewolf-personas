from src.werewolf_crew.crew import WerewolfCrew  # import your CrewAI crew
from dotenv import load_dotenv
import json
from datetime import datetime


class WerewolfGame:
    def __init__(self):
        # Initial state: roles and alive players
        self.players = {
            "Alice": "werewolf",
            "Brian": "werewolf",
            "Achille": "villager",
            "Bethany": "villager",
            "Carol": "villager",
            "Damien": "villager",
            "Ellie": "villager"
        }
        load_dotenv()

        self.eliminated = {}
        self.round_number = 0
        self.transcripts = []
        # Instantiate the CrewAI crew
        self.crew = WerewolfCrew().crew()

    def current_players(self):
        # Return the list of players still alive
        return {p for p in self.players if p not in self.eliminated}

    def prepare_round_input(self):
        players = self.current_players()
        return {
            "players": players,
            "round": self.round_number,
            "eliminated": list(self.eliminated)
        }


    def update_state_from_transcript(self, transcript):
        # Stub: Parse the transcript to determine which player was eliminated.
        day_eliminated_player = self.parse_elimination(transcript)["day_elim"]
        night_eliminated_player = self.parse_elimination(transcript)["night_elim"]

        

        if day_eliminated_player:
            self.eliminated[day_eliminated_player] = True
        if night_eliminated_player:
            self.eliminated[night_eliminated_player] = True

        # Remove eliminated players from playerlist
        self.players = {p for p in self.players if p not in self.eliminated}


    def parse_elimination(self, transcript):
        """
        Transforms a transcript string in JSON format into a Python dictionary.
        It removes any characters before the first '{' or after the last '}'.

        Expected JSON format:
        {
            "transcript": "NIGHT PHASE\nAlice: *gestures to Elle* ...",
            "night_elim": "Villager C",
            "day_elim": "Damien",
            "remaining": ["Alice", "Brian", "Achille", "Bethany", "Ellie"]
        }

        Returns:
            dict: A dictionary with keys 'transcript', 'night_elim', 'day_elim', and 'remaining'.
        """
        # Use transcript.raw if available, otherwise assume transcript is a string.
        transcript_str = transcript.raw if hasattr(transcript, "raw") else transcript

        # Find the substring starting from the first '{' to the last '}'.
        start_index = transcript_str.find('{')
        end_index = transcript_str.rfind('}')
        if start_index == -1 or end_index == -1:
            raise ValueError("No valid JSON object found in transcript")
        
        json_str = transcript_str[start_index:end_index + 1]

        try:
            parsed = json.loads(json_str)
            return parsed
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing transcript JSON: {e}") from e

    
    def play_round(self):

        print("Players in this Round: ", self.players)

        # Funnel input to CrewAI: build and pass context.
        round_input = self.prepare_round_input()
        transcript = self.crew.kickoff(inputs=round_input)

        
        # Append transcript to stored transcripts
        self.transcripts.append(transcript)
        self.update_state_from_transcript(transcript)
        self.round_number += 1

        # Write transcript to file

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"logs/{timestamp}_round_{self.round_number}_transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript.raw)


        return transcript


    def game_over(self):
        """
        Determines if the game is over based on the remaining players.
        
        The game is over if:
        - There is one or zero players left.
        - Only werewolves or only villagers remain.
        
        Returns:
            bool: True if the game is over, False otherwise.
        """
        if len(self.players) <= 1:
            return True

        roles = set(self.players.values())
        if len(roles) == 1:  # All players have the same role (only villagers or only werewolves)
            return True

        return False


def main():
    game = WerewolfGame()
    while not game.game_over():
        transcript = game.play_round()
        print(f"Round {game.round_number} transcript:\n{transcript}\n")

if __name__ == "__main__":
    main()
