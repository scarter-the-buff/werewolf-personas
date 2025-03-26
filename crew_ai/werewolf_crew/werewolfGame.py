from src.werewolf_crew.crew import WerewolfCrew  # import your CrewAI crew
from dotenv import load_dotenv
import json
from datetime import datetime
import sys
import os
import csv



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
        return {p: role for p, role in self.players.items() if p not in self.eliminated}


    def prepare_round_input(self):
        players = self.current_players()
        print("This is players.keys(): ", list(players.keys()))
        return {
            "players": list(players.keys()),
            "round": self.round_number,
            "eliminated": list(self.eliminated)
        }


    def update_state_from_transcript(self, transcript):
        day_eliminated_player = self.parse_elimination(transcript)["day_elim"]
        night_eliminated_player = self.parse_elimination(transcript)["night_elim"]


        print("PARSING TRANSCRIPT: ")

        print("Day Eliminated Player: ", day_eliminated_player)
        print("Night Eliminated Player: ", night_eliminated_player)


        self.eliminated[day_eliminated_player] = True
        self.eliminated[night_eliminated_player] = True

        # Remove eliminated players from playerlist
        print("Self.players before elimination calculation: ", self.players)
        print("Players eliminated: ", self.eliminated)
        self.players = {p: role for p, role in self.players.items() if p not in self.eliminated}


        print("self.players after elimination calculation:", self.players)
 

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
        # print("Players in this Round: ", self.players)

        # Prepare log file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"logs/{timestamp}_round_{self.round_number}_full_log.md"
        os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists

        # Redirect stdout to log file
        original_stdout = sys.stdout
        with open(log_filename, "w", encoding="utf-8") as log_file:
            sys.stdout = log_file  # Redirect stdout

            try:
                # Funnel input to CrewAI: build and pass context.
                round_input = self.prepare_round_input()

                # Run the CrewAI process
                transcript = self.crew.kickoff(inputs=round_input)

                # Append transcript to stored transcripts
                self.transcripts.append(transcript)
                self.update_state_from_transcript(transcript)
                self.round_number += 1

                # Write full transcript to a separate file
                transcript_filename = f"logs/{timestamp}_round_{self.round_number}_output .txt"
                with open(transcript_filename, "w", encoding="utf-8") as f:
                    f.write(transcript.raw)



            finally:
                # Restore stdout
                sys.stdout = original_stdout 

        return transcript
    
    def log_game_over(self, winning_team, num_villagers, num_werewolves):
        """
        Appends a row to 'logs/game_over_log.csv' with the following columns:
        ID, Timestamp, WinningTeam, RemainingVillagers, RemainingWerewolves.
        """
        csv_file = "logs/game_stats.csv"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Ensure the logs directory exists.
        os.makedirs("logs", exist_ok=True)
        
        # Determine the new row's ID.
        row_id = 1
        if os.path.exists(csv_file):
            with open(csv_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                if rows and rows[-1][0].isdigit():
                    row_id = int(rows[-1][0]) + 1

        # Open the CSV file in append mode.
        file_exists = os.path.exists(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # If the file didn't exist, write a header first.
            if not file_exists or os.path.getsize(csv_file) == 0:
                writer.writerow(["ID", "Timestamp", "WinningTeam", "RemainingVillagers", "RemainingWerewolves"])
            writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves])


    def game_over(self):
        """
        Determines if the game is over based on the remaining players.
        The game is over if:
        - There is one or zero players left.
        - Only werewolves or only villagers remain.
        
        When the game is over, a row is appended to a CSV file with:
        ID, Timestamp, WinningTeam, RemainingVillagers, RemainingWerewolves

        Returns:
            bool: True if the game is over, False otherwise.
        """
        # Case 1: Only one or zero players remain.
        if len(self.players) <= 1:
            if self.players:
                # Get the role of the last remaining player.
                last_role = list(self.players.values())[0]
                winning_team = 0 if last_role == "villager" else 1
            else:
                # If no players remain, choose a default (you might adjust this logic).
                winning_team = -1  
            num_villagers = sum(1 for role in self.players.values() if role == "villager")
            num_werewolves = sum(1 for role in self.players.values() if role == "werewolf")
            
            self.log_game_over(winning_team, num_villagers, num_werewolves)
            print("GAME OVER: Only one (or zero) player remains.")
            return True

        # Case 2: All remaining players have the same role.
        roles = set(self.players.values())
        num_left = len(self.players)
        if len(roles) == 1:
            # Determine winning team: 0 for villagers, 1 for werewolves.
            winning_team = 0 if "villager" in roles else 1
            num_villagers = sum(1 for role in self.players.values() if role == "villager")
            num_werewolves = sum(1 for role in self.players.values() if role == "werewolf")
            self.log_game_over(winning_team, num_villagers, num_werewolves)
            if winning_team == 1:
                print(f"GAME OVER: Only werewolves remain, of which there are {num_left}")
            else:
                print(f"GAME OVER: Only villagers remain, of which there are {num_left}")
            return True

        return False

def play_game():
    game = WerewolfGame()
    while not game.game_over():
        game.play_round()

def main():
    for i in range(15): 
        print(f'Game {i+1}')
        print('====================')
        play_game()

if __name__ == "__main__":
    main()
