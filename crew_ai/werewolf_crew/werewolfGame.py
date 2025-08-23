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
from src.werewolf_crew.my_tools import clear_votes_func


# Import logparser
import parser.logparser

# As a preliminary experiment, we'll have two sets of villagers: a set with diverse personalities and a set with homogeneous personalities.
# We'll see which one performs better. 

# TODO: Put these settings in a different file
diverse_v = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "TJ"],
    "Tallier": []
}

all_v_tp = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"],
    "Tallier": []
}

all_v_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"],
    "Tallier": []
}

all_v_fp = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"],
    "Tallier": []
}

all_v_fj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"],
    "Tallier": []
}

villagers_throw = {
    "Player 1": ["werewolf", "blank"],
    "Player 2": ["werewolf", "blank"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Player 5": ["villager", "not_trying_villager"],
    "Player 6": ["villager", "not_trying_villager"],
    "Player 7": ["villager", "not_trying_villager"],
    "Tallier": []
}

v_aggro_were_throw = {
    "Player 1": ["werewolf", "not_trying_werewolf"],
    "Player 2": ["werewolf", "not_trying_werewolf"],
    "Player 3": ["villager", "aggressive_villager"],
    "Player 4": ["villager", "aggressive_villager"],
    "Player 5": ["villager", "aggressive_villager"],
    "Player 6": ["villager", "aggressive_villager"],
    "Player 7": ["villager", "aggressive_villager"],
    "Tallier": []
}

w_aggro_vill_throw = {
    "Player 1": ["werewolf", "aggressive_werewolf"],
    "Player 2": ["werewolf", "aggressive_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Player 5": ["villager", "not_trying_villager"],
    "Player 6": ["villager", "not_trying_villager"],
    "Player 7": ["villager", "not_trying_villager"],
    "Tallier": []
}

werewolves_throw = {
    "Player 1": ["werewolf", "not_trying_werewolf"],
    "Player 2": ["werewolf", "not_trying_werewolf"],
    "Player 3": ["villager", "blank "],
    "Player 4": ["villager", "blank"],
    "Player 5": ["villager", "blank"],
    "Player 6": ["villager", "blank"],
    "Player 7": ["villager", "blank"],
    "Tallier": []
}

alternate_letters = {
    "Player 1": ["werewolf", "alt"],
    "Player 2": ["werewolf", "alt"],
    "Player 3": ["villager", "alt"],
    "Player 4": ["villager", "alt"],
    "Player 5": ["villager", "alt"],
    "Player 6": ["villager", "alt"],
    "Player 7": ["villager", "alt"],
    "Tallier": []
}

alternate_letters_fourp = {
    "Player 1": ["werewolf", "alt"],
    "Player 2": ["werewolf", "alt"],
    "Player 3": ["villager", "alt"],
    "Player 4": ["villager", "alt"],
    "Tallier": []
}

w_aggro_vill_throw_fourp = {
    "Player 1": ["werewolf", "aggressive_werewolf"],
    "Player 2": ["werewolf", "aggressive_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Tallier": []
}

setting_list = [
    # diverse_v,  # Diverse villagers setting
    all_v_tp,   # All villagers with TP personality
    all_v_tj,   # All villagers with TJ personality
    all_v_fp,   # All villagers with FP personality
    all_v_fj    # All villagers with FJ personality
]

import re



class WerewolfGame:

    # Initialize gameCrew

    def __init__(self, curr_setting, curr_setting_name):
        self.players, self.starting_players = curr_setting, curr_setting
        load_dotenv()
        self.eliminated = {}
        self.current_players = self.players
        self.round_number = 0
        self.transcripts = []
        self.curr_setting = curr_setting
        self.curr_setting_name = curr_setting_name

        # initialize Crew
        open("./memories/memory.txt", "a").close()
        self.gameCrew = WerewolfCrew(self.players)
        self.crew = self.gameCrew.crew()

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


        # Filter alive agents at kickoff
        alive_players = self.current_players.keys()

        print("Alive players: ", alive_players)

        self.gameCrew.agents = [a for a in self.gameCrew.agents if a.role in alive_players]

        print("self.crew.agents: ", self.gameCrew.agents)


        # Run the CrewAI process
        # TODO: Tie each task to its own player, and only do each task if the player it corresponds to is actually in the lsit of self.crew.agents

        transcript = self.gameCrew.run_alive_player_tasks(self.current_players.keys())

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
    
        # === ADD inside WerewolfGame ================================================
    def play_round_with_night(self):
            start_time = time.perf_counter()

            # -------- NIGHT --------
            alive_players = [p for p in self.current_players.keys()]
            night = self.gameCrew.run_night_phase_collect(alive_players, self.current_players)

            night_elim = night["night_elim"] or ""
            if night_elim and night_elim in self.current_players and night_elim != "Tallier":
                self.eliminated[night_elim] = True
                self.current_players = {p: role for p, role in self.players.items() if p not in self.eliminated}

            # -------- DAY ----------
            alive_players_after_night = [p for p in self.current_players.keys()]
            day = self.gameCrew.run_day_phase_collect(alive_players_after_night)


            day_elim = day["day_elim"] or ""
            if day_elim and day_elim in self.current_players and day_elim != "Tallier":
                self.eliminated[day_elim] = True
                self.current_players = {p: role for p, role in self.players.items() if p not in self.eliminated}

            # Build a combined JSON you can still persist (mirrors your previous structure)
            combined = {
                "transcript": "",  # no longer useful; agents just output names
                "night_elim": night_elim,
                "day_elim": day_elim,
                "night_votes": night["votes"],
                "day_votes": day["votes"],
                "remaining": [p for p in self.current_players.keys() if p != "Tallier"]
            }

            # Persist for debugging/analysis
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs("memories", exist_ok=True)
            with open(f"memories/{timestamp}.json", "w", encoding="utf-8") as f:
                json.dump(combined, f, ensure_ascii=False, indent=4)

            end_time = time.perf_counter()
            execution_time = end_time - start_time
            os.makedirs("transcripts", exist_ok=True)
            with open(f"transcripts/{timestamp}_round_{self.round_number+1}.txt", "w", encoding="utf-8") as f:
                f.write(json.dumps(combined, ensure_ascii=False, indent=2))
                f.write(f"\n\nRound Execution Time: {execution_time:.6f} seconds\n")

            # push into your old arrays to keep rest of code happy
            self.transcripts.append(json.dumps(combined))
            self.round_number += 1
            return combined


    def log_game_over(self, winning_team, num_villagers, num_werewolves):
        """
        Appends a row to 'logs/game_over_log.csv' with the following columns:
        ID, Timestamp, WinningTeam, RemainingVillagers, RemainingWerewolves.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = f"stats/game_stats_{self.curr_setting_name}.csv"

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
            wa_type = self.starting_players["Player 1"][1]
            wb_type = self.starting_players["Player 2"][1]
            va_type = self.starting_players["Player 3"][1]
            vb_type = self.starting_players["Player 4"][1]
            # vc_type = self.starting_players["Player 5"][1]
            # vd_type = self.starting_players["Player 6"][1]
            # ve_type = self.starting_players["Player 7"][1]

            # If the file didn't exist, write a header first.
            if not file_exists or os.path.getsize(csv_file) == 0:
                writer.writerow(["ID", "Timestamp", "WinningTeam", "RemainingVillagers", "RemainingWerewolves", "wa_type", "wb_type", "va_type", "vb_type", "vc_type", "vd_type", "ve_type"])
            # writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves, wa_type, wb_type, va_type, vb_type, vc_type, vd_type, ve_type])
            writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves, wa_type, wb_type, va_type, vb_type])


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

        # Clear memory JSON for this round
        clear_votes_func("day")
        clear_votes_func("night")


        print("PERFORMING GAME OVER")
        players = self.current_players
        # Case 1: Only one or zero players remain.
        # We must subtract one to represent the tallier
        if len(players ) - 1 <= 1:
            print("GAME OVER: First Branch")
            role_data = [data[0] for data in players.values() if data]

            if players:
                # Get the role of the last remaining player.
                try:
                    last_role = list(set(role_data))[0]
                except: 
                    # This will cause an error if there are no more roles
                    last_role = ""
                print("Last role: ", last_role)
                if last_role == "villager":
                    winning_team = "V"
                elif last_role == "werewolf":
                    winning_team = "W"
                else:
                    winning_team = "N"
                print(f"The last remaining player is {list(players.keys())[0]} with role {last_role}.")
            else:
                winning_team = "N"  


            print("Role data: ", role_data)
            
            num_villagers = sum([1 for role in role_data if role == "villager"])
            num_werewolves = sum([1 for role in role_data if role == "werewolf"])

            print("num_villagers: ", num_villagers)
            print("num_werewolves: ", num_werewolves)

            self.log_game_over(winning_team, num_villagers, num_werewolves)
            print("GAME OVER: Only one (or zero) player remains.")
            return True
        # Case 2: All remaining non-Tallier players have the same role.
        role_data = [vals[0] for name, vals in players.items() if name != "Tallier" and vals]
        roles_set = set(role_data)
        print("Roles: ", roles_set)

        if len(roles_set) == 1:
            print("GAME OVER: Second Branch")

            # Determine winning team from the single role present
            only_role = next(iter(roles_set)) if roles_set else ""
            winning_team = "V" if only_role == "villager" else ("W" if only_role == "werewolf" else "N")

            num_villagers = sum(1 for r in role_data if r == "villager")
            num_werewolves = sum(1 for r in role_data if r == "werewolf")

            self.log_game_over(winning_team, num_villagers, num_werewolves)

            num_left = len([n for n in players.keys() if n != "Tallier"])
            if winning_team == "W":
                print(f"GAME OVER: Only werewolves remain, of which there are {num_left}")
            elif winning_team == "V":
                print(f"GAME OVER: Only villagers remain, of which there are {num_left}")
            else:
                print(f"GAME OVER: All remaining have the same nonstandard role: {only_role}")
            return True
        return False
    
    def check_game_over(self):
        players = self.current_players
        roles = (set([player[0] for player in list(players.values()) if player != []]))
        if len(roles) == 1:
            print("Check game over detected game over")
            return True
        else: 
            print("Check game over detected no game over")
            return False

def play_game():

    # Start by clearing the JSON memory, in case the last game failed to finish

    clear_votes_func("night")
    clear_votes_func("day")


    game = WerewolfGame(curr_setting, curr_setting_name)
    # Subtract one for Tallier; another ensures at least one remains
    round_num = len(game.crew.agents) - 2

    for i in range(round_num):
        print("==== STARTING ROUND {0} === ".format(i+1))
        game.play_round_with_night()
        print("Finished Round {0}".format(i+1))
        if game.check_game_over():
            print("Game Over.")
            break

    game_over_result = game.game_over()
    print(f"Game Over? {game_over_result}")


def main():
    game_num = 1

    # Set the current villagers for the game instance
    global curr_setting
    curr_setting = w_aggro_vill_throw 
    global curr_setting_name
    curr_setting_name = "w_aggro_vill_throw"

    
    
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
