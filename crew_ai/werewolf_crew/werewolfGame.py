from src.werewolf_crew.crew import WerewolfCrew  # import your CrewAI crew
from dotenv import load_dotenv
import json
from datetime import datetime
import sys
import os
import csv
import time # Timer to time round execution for optimization purposes


# As a preliminary experiment, we'll have two sets of villagers: a set with diverse personalities and a set with homogeneous personalities.
# We'll see which one performs better. 

# TODO: Add small-team versions to all of these modes
diverse_v = {
            "Alice": ["werewolf", "TJ"],
            "Brian": ["werewolf", "FP"],
            "Alex": ["villager", "TJ"],
            "Bethany": ["villager", "TP"],
            "Carol": ["villager", "FJ"],
            "Damien": ["villager", "FP"],
            "Ellie": ["villager", "TJ"]
        }

all_v_tp = {
            "Alice": ["werewolf", "TJ"],
            "Brian": ["werewolf", "FP"],
            "Alex": ["villager", "TP"],
            "Bethany": ["villager", "TP"],
            "Carol": ["villager", "TP"],
            "Damien": ["villager", "TP"],
            "Ellie": ["villager", "TP"]
}

all_v_tj = {
    "Alice": ["werewolf", "TJ"],
    "Brian": ["werewolf", "FP"],
    "Alex": ["villager", "TJ"],
    "Bethany": ["villager", "TJ"],
    "Carol": ["villager", "TJ"],
    "Damien": ["villager", "TJ"],
    "Ellie": ["villager", "TJ"]
}

all_v_fp = {
    "Alice": ["werewolf", "TJ"],
    "Brian": ["werewolf", "FP"],
    "Alex": ["villager", "FP"],
    "Bethany": ["villager", "FP"],
    "Carol": ["villager", "FP"],
    "Damien": ["villager", "FP"],
    "Ellie": ["villager", "FP"]
}

all_v_fj = {
    "Alice": ["werewolf", "TJ"],
    "Brian": ["werewolf", "FP"],
    "Alex": ["villager", "FJ"],
    "Bethany": ["villager", "FJ"],
    "Carol": ["villager", "FJ"],
    "Damien": ["villager", "FJ"],
    "Ellie": ["villager", "FJ"]
}

villagers_throw = {
    "Alice": ["werewolf", "blank"],
    "Brian": ["werewolf", "blank"],
    "Alex": ["villager", "not_trying_villager"],
    "Bethany": ["villager", "not_trying_villager"],
    "Carol": ["villager", "not_trying_villager"],
    "Damien": ["villager", "not_trying_villager"],
    "Ellie": ["villager", "not_trying_villager"]
}

v_aggro_were_throw = {
    "Alice": ["werewolf", "not_trying_werewolf"],
    "Brian": ["werewolf", "not_trying_werewolf"],
    "Alex": ["villager", "aggressive_villager"],
    "Bethany": ["villager", "aggressive_villager"],
    "Carol": ["villager", "aggressive_villager"],
    "Damien": ["villager", "aggressive_villager"],
    "Ellie": ["villager", "aggressive_villager"]
}

w_aggro_vill_throw = {
    "Alice": ["werewolf", "aggressive_werewolf"],
    "Brian": ["werewolf", "aggressive_werewolf"],
    "Alex": ["villager", "not_trying_villager"],
    "Bethany": ["villager", "not_trying_villager"],
    "Carol": ["villager", "not_trying_villager"],
    "Damien": ["villager", "not_trying_villager"],
    "Ellie": ["villager", "not_trying_villager"]
}

werewolves_throw = {
    "Alice": ["werewolf", "not_trying_werewolf"],
    "Brian": ["werewolf", "not_trying_werewolf"],
    "Alex": ["villager", "blank "],
    "Bethany": ["villager", "blank"],
    "Carol": ["villager", "blank"],
    "Damien": ["villager", "blank"],
    "Ellie": ["villager", "blank"]
}


alternate_letters = {
    "Alice": ["werewolf", "alt"],
    "Brian": ["werewolf", "alt"],
    "Alex": ["villager", "alt"],
    "Bethany": ["villager", "alt"],
    "Carol": ["villager", "alt"],
    "Damien": ["villager", "alt"],
    "Ellie": ["villager", "alt"]
}

alternate_letters_fourp = {
    "Alice": ["werewolf", "alt"],
    "Brian": ["werewolf", "alt"],
    "Alex": ["villager", "alt"],
    "Bethany": ["villager", "alt"]
}

setting_list = [
    # diverse_v,  # Diverse villagers setting
    all_v_tp,   # All villagers with TP personality
    all_v_tj,   # All villagers with TJ personality
    all_v_fp,   # All villagers with FP personality
    all_v_fj    # All villagers with FJ personality
]


class WerewolfGame:
    def __init__(self):
        # Initial state: roles and alive players
        self.players = curr_setting
        self.starting_players = self.players
        load_dotenv()

        self.eliminated = {}
        self.round_number = 0
        self.transcripts = []
        # Instantiate the CrewAI crew
        gameCrew = WerewolfCrew(self.players)
        self.crew = gameCrew.crew()

    def current_players(self):
        # Return the list of players still alive
        return {p: role for p, role in self.players.items() if p not in self.eliminated}


    def prepare_round_input(self):
        players = self.current_players()
        # print("This is players.keys(): ", list(players.keys()))

        # Print all agent personalities to confirm that they've been properly initialized
        # print("Printing all agent backstories for the current round:")
        # for i in range(1, len(self.crew.agents)):
        #     agent = self.crew.agents[i]
        #     print(f"Agent {i}: " + agent.backstory + "\n")
        # print("End personality reporting.")


        return {
            "players": list(players.keys()),
            "round": self.round_number,
            "eliminated": list(self.eliminated)
        }


    def update_state_from_transcript(self, transcript):
        day_eliminated_player = self.parse_elimination(transcript)["day_elim"]
        night_eliminated_player = self.parse_elimination(transcript)["night_elim"]


        # print("PARSING TRANSCRIPT: ")

        # print("Day Eliminated Player: ", day_eliminated_player)
        # print("Night Eliminated Player: ", night_eliminated_player)


        self.eliminated[day_eliminated_player] = True
        self.eliminated[night_eliminated_player] = True

        # Remove eliminated players from playerlist
        # print("Self.players before elimination calculation: ", self.players)
        # print("Players eliminated: ", self.eliminated)
        self.players = {p: role for p, role in self.players.items() if p not in self.eliminated}


        # print("self.players after elimination calculation:", self.players)
 

    def parse_elimination(self, transcript):
        """
        Transforms a transcript string in JSON format into a Python dictionary.
        It removes any characters before the first '{' or after the last '}'.

        Expected JSON format:
        {
            "transcript": "NIGHT PHASE\nAlice: *gestures to Elle* ...",
            "night_elim": "Villager C",
            "day_elim": "Damien",
            "remaining": ["Alice", "Brian", "Alex", "Bethany", "Ellie"]
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
            print("Error from the following transcript string: ", transcript_str)  # Debugging line to see the input
            raise ValueError(f"Error parsing transcript JSON: {e}") from e

    

    def play_round(self):
        # print("Players in this Round: ", self.players)

        # Start measuring execution time
        start_time = time.perf_counter()


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

                # Record end time
                end_time = time.perf_counter()
                execution_time = end_time - start_time


                # Write full transcript to a separate file
                transcript_filename = f"logs/{timestamp}_round_{self.round_number}_output .txt"
                with open(transcript_filename, "w", encoding="utf-8") as f:
                    f.write(transcript.raw)
                    f.write(f"\n Round Execution Time: {execution_time:.6f} seconds \n")



            finally:
                # Restore stdout
                sys.stdout = original_stdout 


        return transcript
    
    def log_game_over(self, winning_team, num_villagers, num_werewolves):
        """
        Appends a row to 'logs/game_over_log.csv' with the following columns:
        ID, Timestamp, WinningTeam, RemainingVillagers, RemainingWerewolves.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = f"stats/game_stats_{curr_setting_name}.csv"

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


        # print("Inputs to logging game over: ")
        # print(f"Winning Team: {winning_team}")
        # print(f"Number of Villagers Remaining: {num_villagers}")
        # print(f"Number of Werewolves Remaining: {num_werewolves}")
        
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

            # Record player personality types
            wa_type = self.starting_players["Alice"][1]
            wb_type = self.starting_players["Brian"][1]
            va_type = self.starting_players["Alex"][1]
            vb_type = self.starting_players["Bethany"][1]
            vc_type = self.starting_players["Carol"][1]
            vd_type = self.starting_players["Damien"][1]
            ve_type = self.starting_players["Ellie"][1]

            # If the file didn't exist, write a header first.
            if not file_exists or os.path.getsize(csv_file) == 0:
                writer.writerow(["ID", "Timestamp", "WinningTeam", "RemainingVillagers", "RemainingWerewolves", "wa_type", "wb_type", "va_type", "vb_type", "vc_type", "vd_type", "ve_type"])
            writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves, wa_type, wb_type, va_type, vb_type, vc_type, vd_type, ve_type])


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
                last_role = list(self.players.values())[0][0]
                print("Last role: ", last_role)
                winning_team = 0 if last_role == "villager" else 1
                print(f"The last remaining player is {list(self.players.keys())[0]} with role {last_role}.")
            else:
                winning_team = -1  
            
            num_villagers = sum(1 for role_data in self.players.values() if role_data[0] == "villager")
            num_werewolves = sum(1 for role_data in self.players.values() if role_data[0] == "werewolf")

                        
            self.log_game_over(winning_team, num_villagers, num_werewolves)
            print("GAME OVER: Only one (or zero) player remains.")
            return True

        # Case 2: All remaining players have the same role.
        roles = set([self.players[i][0] for i in self.players])
        print("Roles in the game: ", roles)
        num_left = len(self.players)
        if len(roles) == 1:
            # Determine winning team: 0 for villagers, 1 for werewolves.
            winning_team = 0 if "villager" in roles else 1

            num_villagers = sum(1 for role_data in self.players.values() if role_data[0] == "villager")
            num_werewolves = sum(1 for role_data in self.players.values() if role_data[0] == "werewolf")

            self.log_game_over(winning_team, num_villagers, num_werewolves)
            if winning_team == 1:
                print(f"GAME OVER: Only werewolves remain, of which there are {num_left}")
            else:
                print(f"GAME OVER: Only villagers remain, of which there are {num_left}")
            return True

        return False

def play_game():
    game = WerewolfGame()
    print("werewolfGame line 380")
    while not game.game_over():
        game.play_round()

def main():
    game_num = 10

    # Set the current villagers for the game instance
    global curr_setting
    curr_setting = alternate_letters_fourp
    global curr_setting_name
    curr_setting_name = "alternate_letters_four_o" 

    for i in range(game_num): 
        print(f'Game {i+1}')
        print('====================')
        play_game()

if __name__ == "__main__":
    main()
