from src.werewolf_crew.crew import WerewolfCrew  # import your CrewAI crew
from src.werewolf_crew.crew import extMem # Import external memory
from dotenv import load_dotenv
import json
from textwrap import indent
from datetime import datetime
import sys
import re
import os
import csv
import time # Timer to time round execution for optimization purposes

# Import logparser
import parser.logparser

# As a preliminary experiment, we'll have two sets of villagers: a set with diverse personalities and a set with homogeneous personalities.
# We'll see which one performs better. 

# TODO: Add small-team versions to all of these modes
diverse_v = {
            "Player 1": ["werewolf", "TJ"],
            "Player 2": ["werewolf", "FP"],
            "Player 3": ["villager", "TJ"],
            "Player 4": ["villager", "TP"],
            "Player 5": ["villager", "FJ"],
            "Player 6": ["villager", "FP"],
            "Player 7": ["villager", "TJ"]
        }

all_v_tp = {
            "Player 1": ["werewolf", "TJ"],
            "Player 2": ["werewolf", "FP"],
            "Player 3": ["villager", "TP"],
            "Player 4": ["villager", "TP"],
            "Player 5": ["villager", "TP"],
            "Player 6": ["villager", "TP"],
            "Player 7": ["villager", "TP"]
}

all_v_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}

all_v_fp = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
}

all_v_fj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

villagers_throw = {
    "Player 1": ["werewolf", "blank"],
    "Player 2": ["werewolf", "blank"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Player 5": ["villager", "not_trying_villager"],
    "Player 6": ["villager", "not_trying_villager"],
    "Player 7": ["villager", "not_trying_villager"]
}

v_aggro_were_throw = {
    "Player 1": ["werewolf", "not_trying_werewolf"],
    "Player 2": ["werewolf", "not_trying_werewolf"],
    "Player 3": ["villager", "aggressive_villager"],
    "Player 4": ["villager", "aggressive_villager"],
    "Player 5": ["villager", "aggressive_villager"],
    "Player 6": ["villager", "aggressive_villager"],
    "Player 7": ["villager", "aggressive_villager"]
}

w_aggro_vill_throw = {
    "Player 1": ["werewolf", "aggressive_werewolf"],
    "Player 2": ["werewolf", "aggressive_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Player 5": ["villager", "not_trying_villager"],
    "Player 6": ["villager", "not_trying_villager"],
    "Player 7": ["villager", "not_trying_villager"]
}

werewolves_throw = {
    "Player 1": ["werewolf", "not_trying_werewolf"],
    "Player 2": ["werewolf", "not_trying_werewolf"],
    "Player 3": ["villager", "blank "],
    "Player 4": ["villager", "blank"],
    "Player 5": ["villager", "blank"],
    "Player 6": ["villager", "blank"],
    "Player 7": ["villager", "blank"]
}


alternate_letters = {
    "Player 1": ["werewolf", "alt"],
    "Player 2": ["werewolf", "alt"],
    "Player 3": ["villager", "alt"],
    "Player 4": ["villager", "alt"],
    "Player 5": ["villager", "alt"],
    "Player 6": ["villager", "alt"],
    "Player 7": ["villager", "alt"]
}

alternate_letters_fourp = {
    "Player 1": ["werewolf", "alt"],
    "Player 2": ["werewolf", "alt"],
    "Player 3": ["villager", "alt"],
    "Player 4": ["villager", "alt"]
}



w_aggro_vill_throw_fourp = {
    "Player 1": ["werewolf", "aggressive_werewolf"],
    "Player 2": ["werewolf", "aggressive_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"]
}

setting_list = [
    # diverse_v,  # Diverse villagers setting
    all_v_tp,   # All villagers with TP personality
    all_v_tj,   # All villagers with TJ personality
    all_v_fp,   # All villagers with FP personality
    all_v_fj    # All villagers with FJ personality
]

import re

# TODO: UNUSED, LIKELY DELETE CANDIDATE
def parse_and_pretty_print(data: str) -> str:
    # Remove unreadable/control characters (non-printable except basic whitespace)
    cleaned = re.sub(r'[^\x20-\x7E\n\t]', '', data)

    # Normalize curly quotes to straight quotes
    cleaned = cleaned.replace("“", '"').replace("”", '"').replace("’", "'")

    # Collapse multiple spaces/tabs into a single space
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in cleaned.splitlines()]

    # Remove empty lines except single spacing
    pretty_transcript = "\n".join(line for line in lines if line)

    return pretty_transcript


class WerewolfGame:
    def __init__(self):
        # Initial state: roles and alive players
        self.players, self.starting_players = curr_setting, curr_setting
        load_dotenv()

        self.eliminated = {}
        self.current_players = self.players
        self.round_number = 0
        self.transcripts = []
        # Instantiate the CrewAI crew
        gameCrew = WerewolfCrew(self.players)
        self.crew = gameCrew.crew()


    def prepare_round_input(self):
        players = self.current_players
        # print("This is players.keys(): ", list(players.keys()))

        # Print all agent personalities to confirm that they've been properly initialized
        # print("Printing all agent backstories for the current round:")
        # for i in range(1, len(self.crew.agents)):
        #     agent = self.crew.agents[i]
        #     print(f"Agent {i}: " + agent.backstory + "\n")
        # print("End personality reporting.")

        # Tell the agents which players they can vote for
        for i in range(1, len(self.crew.tasks) - 1):
            task = self.crew.tasks[i]
            print("players: ", players.keys())
            available_choices =  " You can only choose one of the following remaining players to eliminate: " + ', '.join(players.keys())
            task.expected_output += available_choices
            self.crew.tasks[i] = task
            print("In pr")
            

        return {
            "players": list(players.keys()),
            "round": self.round_number,
            "eliminated": list(self.eliminated)
        }


    def update_state_from_transcript(self, transcript):
        # TODO: Parse the new type of transcript here.

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
        self.current_players = {p: role for p, role in self.players.items() if p not in self.eliminated}



        print("self.current_players after elimination calculation:", self.current_players)
 

    def parse_elimination(self, transcript):
        """
        Transforms a transcript string in JSON format into a Python dictionary.
        It removes any characters before the first '{' or after the last '}'.

        Expected JSON format:
        {
            "transcript": "NIGHT PHASE\nPlayer 1: *gestures to Elle* ...",
            "night_elim": "Villager C",
            "day_elim": "Player 6",
            "remaining": ["Player 1", "Player 2", "Player 3", "Player 4", "Player 7"]
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

        # Funnel input to CrewAI: build and pass context.
        round_input = self.prepare_round_input()

        # Filter alive agents at kickoff
        alive_players = set(self.current_players.keys())

        print("Alive players: ", alive_players)

        agents = self.crew.agents
        self.crew.agents = [a for a in self.crew.agents if a.role in alive_players]

        print("self.crew.agents: ", self.crew.agents)


        # Run the CrewAI process
        transcript = self.crew.kickoff(inputs=round_input)

        # Record memory after each round

        # Create filename with current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"memories/{timestamp}.json"

        # Post-round read from external memory
        print("POST-ROUND: READING FROM EXTERNAL MEMORY: ", extMem.storage.memories)

        # Save to file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(extMem.storage.memories, f, ensure_ascii=False, indent=4)
        
        print("In play_round: round transcript: ", transcript)


        # Update state from transcript
        self.transcripts.append(transcript)
        self.update_state_from_transcript(transcript)
        self.round_number += 1

        # Record end time
        end_time = time.perf_counter()
        execution_time = end_time - start_time


        # Write full transcript to a separate file
        transcript_filename = f"transcripts/{timestamp}_round_{self.round_number}_transcript .txt"
        with open(transcript_filename, "w", encoding="utf-8") as f:
            f.write(transcript.raw)

            # Write prettier version of the transcript
            f.write("\n===TRANSCRIPT===\n")
            f.write(transcript.raw)

            # Write round execution time
            f.write(f"\n Round Execution Time: {execution_time:.6f} seconds \n")




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
            wa_type = self.starting_players["Player_1"][1]
            wb_type = self.starting_players["Player_2"][1]
            va_type = self.starting_players["Player 3"][1]
            vb_type = self.starting_players["Player 4"][1]
            vc_type = self.starting_players["Player 5"][1]
            vd_type = self.starting_players["Player 6"][1]
            ve_type = self.starting_players["Player 7"][1]

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
    # while not game.game_over():
    #     game.play_round()

    for i in range(3):
        print("==== STARTING ROUND {0} === ".format(i))
        print("CURRENT PLAYERS: {0}".format(game.players))
        game.play_round()
        print("Finished Round {0}".format(i))

    # TODO: Does telemetry time out here?

def main():
    game_num = 1

    # Set the current villagers for the game instance
    global curr_setting
    curr_setting = w_aggro_vill_throw_fourp
    global curr_setting_name
    curr_setting_name = "w_aggro_vill_throw_fourp"

    
    
    # Prepare log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"logs/{timestamp}.ansi"


    # Redirect stdout to log file
    original_stdout = sys.stdout
    with open(log_filename, "w", encoding="utf-8") as log_file:
        sys.stdout = log_file  # Redirect stdout


        for i in range(game_num): 
            print(f'Game {i+1}')
            print('====================')
            play_game()

    # Restore stdout
    sys.stdout = original_stdout 

    # Parser logfile content with logparser
    with open(log_filename, "r", encoding="utf-8") as log_file:
        text = log_file.read()

    cleaned_text = parser.logparser.clean_text(text)

    # Step 3: overwrite the file with cleaned text
    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(cleaned_text)


    

if __name__ == "__main__":
    main()
