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


# Applied control (to account for affects of applying personalities)
applied_control = {
    "Player 1": ["werewolf", "not_trying_werewolf"],
    "Player 2": ["werewolf", "not_trying_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Player 5": ["villager", "not_trying_villager"],
    "Player 6": ["villager", "not_trying_villager"],
    "Player 7": ["villager", "not_trying_villager"]
}

control = {
    "Player 1": ["werewolf", ""],
    "Player 2": ["werewolf", ""],
    "Player 3": ["villager", ""],
    "Player 4": ["villager", ""],
    "Player 5": ["villager", ""],
    "Player 6": ["villager", ""],
    "Player 7": ["villager", ""]
}

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
    "Player 1": ["werewolf", ""],
    "Player 2": ["werewolf", ""],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"]
}

all_v_tj = {
    "Player 1": ["werewolf", ""],
    "Player 2": ["werewolf", ""],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}

all_v_fp = {
    "Player 1": ["werewolf", ""],
    "Player 2": ["werewolf", ""],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
}

all_v_fj = {
    "Player 1": ["werewolf", ""],
    "Player 2": ["werewolf", ""],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

all_w_tp = {
    "Player 1": ["werewolf", "TP"],
    "Player 2": ["werewolf", "TP"],
    "Player 3": ["villager", ""],
    "Player 4": ["villager", ""],
    "Player 5": ["villager", ""],
    "Player 6": ["villager", ""],
    "Player 7": ["villager", ""]
}

all_w_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "TJ"],
    "Player 3": ["villager", ""],
    "Player 4": ["villager", ""],
    "Player 5": ["villager", ""],
    "Player 6": ["villager", ""],
    "Player 7": ["villager", ""]
}

all_w_fp = {
    "Player 1": ["werewolf", "FP"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", ""],
    "Player 4": ["villager", ""],
    "Player 5": ["villager", ""],
    "Player 6": ["villager", ""],
    "Player 7": ["villager", ""]
}

all_w_fj = {
    "Player 1": ["werewolf", "FJ"],
    "Player 2": ["werewolf", "FJ"],
    "Player 3": ["villager", ""],
    "Player 4": ["villager", ""],
    "Player 5": ["villager", ""],
    "Player 6": ["villager", ""],
    "Player 7": ["villager", ""]
}

# Villagers = TP, Werewolves = TJ
v_tp_w_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "TJ"],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"]
}

# Villagers = TJ, Werewolves = TP
v_tj_w_tp = {
    "Player 1": ["werewolf", "TP"],
    "Player 2": ["werewolf", "TP"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}


# Villagers = FJ, Werewolves = TJ
v_fj_w_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "TJ"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

# Villagers = FP, Werewolves = TJ
v_fp_w_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "TJ"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
}

# Villagers = TJ, Werewolves = FJ
v_tj_w_fj = {
    "Player 1": ["werewolf", "FJ"],
    "Player 2": ["werewolf", "FJ"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}

# Villagers = TP, Werewolves = FJ
v_tp_w_fj = {
    "Player 1": ["werewolf", "FJ"],
    "Player 2": ["werewolf", "FJ"],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"]
}

# Villagers = FP, Werewolves = FJ
v_fp_w_fj = {
    "Player 1": ["werewolf", "FJ"],
    "Player 2": ["werewolf", "FJ"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
}

# Villagers = FJ, Werewolves = FP
v_fj_w_fp = {
    "Player 1": ["werewolf", "FP"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

# Villagers = TJ, Werewolves = FP
v_tj_w_fp = {
    "Player 1": ["werewolf", "FP"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}

# Villagers = TP, Werewolves = FP
v_tp_w_fp = {
    "Player 1": ["werewolf", "FP"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"]
}

# Villagers = FJ, Werewolves = TP
v_fj_w_tp = {
    "Player 1": ["werewolf", "TP"],
    "Player 2": ["werewolf", "TP"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

# Villagers = FP, Werewolves = TP
v_fp_w_tp = {
    "Player 1": ["werewolf", "TP"],
    "Player 2": ["werewolf", "TP"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
}

# Mirror matches

# Villagers = TJ, Werewolves = TJ
v_tj_w_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "TJ"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}

# Villagers = TP, Werewolves = TP
v_tp_w_tp = {
    "Player 1": ["werewolf", "TP"],
    "Player 2": ["werewolf", "TP"],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"]
}

# Villagers = FJ, Werewolves = FJ
v_fj_w_fj = {
    "Player 1": ["werewolf", "FJ"],
    "Player 2": ["werewolf", "FJ"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

# Villagers = FP, Werewolves = FP
v_fp_w_fp = {
    "Player 1": ["werewolf", "FP"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
}


# Villagers = TJ, Werewolves = TJ
v_tj_w_tj = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "TJ"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TJ"],
    "Player 5": ["villager", "TJ"],
    "Player 6": ["villager", "TJ"],
    "Player 7": ["villager", "TJ"]
}

# Villagers = TP, Werewolves = TP
v_tp_w_tp = {
    "Player 1": ["werewolf", "TP"],
    "Player 2": ["werewolf", "TP"],
    "Player 3": ["villager", "TP"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "TP"],
    "Player 6": ["villager", "TP"],
    "Player 7": ["villager", "TP"]
}

# Villagers = FJ, Werewolves = FJ
v_fj_w_fj = {
    "Player 1": ["werewolf", "FJ"],
    "Player 2": ["werewolf", "FJ"],
    "Player 3": ["villager", "FJ"],
    "Player 4": ["villager", "FJ"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FJ"],
    "Player 7": ["villager", "FJ"]
}

# Villagers = FP, Werewolves = FP
v_fp_w_fp = {
    "Player 1": ["werewolf", "FP"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "FP"],
    "Player 4": ["villager", "FP"],
    "Player 5": ["villager", "FP"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "FP"]
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
    control,           # No personalities
    diverse_v,         # Diverse villagers setting
    all_v_tp,          # All villagers with TP personality
    all_v_tj,          # All villagers with TJ personality
    all_v_fp,          # All villagers with FP personality
    all_v_fj,          # All villagers with FJ personality
    villagers_throw,   # Villagers throw, werewolves are blank
    werewolves_throw,  # Werewolves throw, villagers are blank
    alternate_letters,  # Alternating personality assignment
    w_aggro_vill_throw,
    v_aggro_were_throw

]

setting_list_shortened = [
    w_aggro_vill_throw,   # Villagers throw, werewolves are blank
    v_aggro_were_throw,  # Werewolves throw, villagers are blank
]

personality_combo_list = [
    v_tp_w_tj,
    v_tj_w_tp,
    v_fj_w_tj,
    v_fp_w_tj,
    v_tj_w_fj,
    v_tp_w_fj,
    v_fp_w_fj,
    v_fj_w_fp,
    v_tj_w_fp,
    v_tp_w_fp,
    v_fj_w_tp,
    v_fp_w_tp
]

mirror_matches = [
    v_tp_w_tp,
    
]

villager_blank_personality_list = []

mirror_matches = [
    v_tj_w_tj,
    v_tp_w_tp,
    v_fj_w_fj,
    v_fp_w_fp
]

mirror_matches_names = [
    "v_tj_w_tj",
    "v_tp_w_tp",
    "v_fj_w_fj",
    "v_fp_w_fp"
]



personality_combo_list_names = [
    "v_tp_w_tj",
    "v_tj_w_tp",
    "v_fj_w_tj",
    "v_fp_w_tj",
    "v_tj_w_fj",
    "v_tp_w_fj",
    "v_fp_w_fj",
    "v_fj_w_fp",
    "v_tj_w_fp",
    "v_tp_w_fp",
    "v_fj_w_tp",
    "v_fp_w_tp"
]

personality_combo_list_short  = [
    v_fj_w_tj,
    v_fp_w_tj,
    v_tj_w_fj,
    v_tp_w_fj,
    v_fp_w_fj,
    v_fj_w_fp,
    v_tj_w_fp,
    v_tp_w_fp,
    v_fj_w_tp,
    v_fp_w_tp
]

personality_combo_list_names_short = [
    "v_fj_w_tj",
    "v_fp_w_tj",
    "v_tj_w_fj",
    "v_tp_w_fj",
    "v_fp_w_fj",
    "v_fj_w_fp",
    "v_tj_w_fp",
    "v_tp_w_fp",
    "v_fj_w_tp",
    "v_fp_w_tp"
]

setting_name_list = [
    "control",
    "villagers_throw",
    "werewolves_throw",
    "w_aggro_vill_throw",
    "v_aggro_were_throw",
    "diverse_v",
    "all_v_tp",
    "all_v_tj",
    "all_v_fp",
    "all_v_fj",
    "villagers_throw",
    "werewolves_throw",
    "w_aggro_vill_throw",
    "v_aggro_were_throw"
]

setting_name_list_shortened = [
    "w_aggro_vill_throw",
    "v_"
    ""
    "aggro_were_throw"
]

control_list = [
    applied_control
]

control_list_names = [
    "applied_control"
]

villager_none_list = [
    all_w_tp,
    all_w_tj,
    all_w_fp,
    all_w_fj
]

villager_none_list_names = [
    "all_w_tp",
    "all_w_tj",
    "all_w_fp",
    "all_w_fj"
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
        self.game_flag = False

        # initialize Crew
        open("./memories/memory.txt", "a").close()
        self.gameCrew = WerewolfCrew(self.players)
        self.crew = self.gameCrew.crew()

    def update_state_from_transcript(self, transcript):
        """
        Parse an elimination transcript from the previous round and update the simulation state.

        This method reads the transcript (produced by earlier day/night vote phases),
        determines which players were eliminated during the day and night, and updates
        the internal bookkeeping:

        - Marks eliminated players in `self.eliminated`.
        - Removes them from `self.current_players` so they no longer participate in future rounds.

        Args:
            transcript: Raw transcript object or string containing elimination information.
                Must be parsable by `self.parse_elimination` to extract `day_elim` and `night_elim`.

        Side Effects:
            - Mutates `self.eliminated` by adding the players eliminated this round.
            - Mutates `self.current_players` to exclude newly eliminated players.
            - Prints debug information about the parsing and updated state.
        """
        # TODO: Parse the new type of transcript here.

        day_eliminated_player = self.parse_elimination(transcript)["day_elim"]
        night_eliminated_player = self.parse_elimination(transcript)["night_elim"]

        print("PARSING TRANSCRIPT: ")
        print("Day Eliminated Player:", day_eliminated_player)
        print("Night Eliminated Player:", night_eliminated_player)

        self.eliminated[day_eliminated_player] = True
        self.eliminated[night_eliminated_player] = True

        # Remove eliminated players from playerlist
        print("Self.players before elimination calculation:", self.players)
        print("Players eliminated:", self.eliminated)
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


    
    def play_round_with_night(self):
        """
        Play one full game round consisting of a night phase and a day phase.

        This method drives the core turn loop of the game:

        1. **Night Phase**
        - Calls `gameCrew.run_night_phase_collect` for all currently alive players.
        - Eliminates the player chosen by werewolves, if any.
        - Immediately checks if the game has ended after the night kill.

        2. **Day Phase**
        - Runs `gameCrew.run_day_phase_collect` for the remaining alive players.
        - Eliminates the player voted out during the day.
        - Checks again for game end conditions.

        3. **Persistence**
        - Builds a combined round summary (JSON-like dict) containing:
            - `"night_elim"`: player killed at night (or empty string).
            - `"day_elim"`: player killed during the day (or empty string).
            - `"night_votes"` / `"day_votes"`: raw vote records for each phase.
            - `"remaining"`: list of players still alive (excluding `"Tallier"`).
        - Saves this summary to `memories/` as a `.json` file and to
            `transcripts/` as a `.txt` file with timing information.
        - Appends the summary to `self.transcripts` and increments `self.round_number`.

        Game-over detection is performed after both phases by calling
        `check_game_over()` and, if true, sets `self.game_flag` to False
        and calls `do_game_over()`.

        Returns:
            dict: Combined round summary with keys:
                - `"transcript"` (str): Placeholder (empty).
                - `"night_elim"` (str): Player name eliminated at night, or "".
                - `"day_elim"` (str): Player name eliminated during the day, or "".
                - `"night_votes"` (list[dict]): Vote records from the night phase.
                - `"day_votes"` (list[dict]): Vote records from the day phase.
                - `"remaining"` (list[str]): Players still alive (excluding Tallier).

        Side Effects:
            - Mutates `self.eliminated` and `self.current_players`.
            - Writes JSON and text files under `memories/` and `transcripts/`.
            - Prints debug/logging information.
            - Updates `self.transcripts`, `self.round_number`, and `self.game_flag`.
        """
        start_time = time.perf_counter()

        # -------- NIGHT --------
        alive_players = [p for p in self.current_players.keys()]
        night = self.gameCrew.run_night_phase_collect(alive_players, self.current_players)


        night_elim = night["night_elim"] or ""
        if night_elim and night_elim in self.current_players and night_elim != "Tallier":
            self.eliminated[night_elim] = True
            self.current_players = {p: role for p, role in self.players.items() if p not in self.eliminated}
        
        # The last villager could have been eliminated during this night phase, so once the players are eliminated we check for game over
        if self.check_game_over():
            print("Game Over.")
            self.game_flag = False
            self.do_game_over()
            return
            

        # -------- DAY ----------
        alive_players_after_night = [p for p in self.current_players.keys()]
        day = self.gameCrew.run_day_phase_collect(alive_players_after_night)


        day_elim = day["day_elim"] or ""
        if day_elim and day_elim in self.current_players and day_elim != "Tallier":
            self.eliminated[day_elim] = True
            self.current_players = {p: role for p, role in self.players.items() if p not in self.eliminated}

        # Check for game over
        if self.check_game_over():
            print("Game Over.")
            self.game_flag = False
            self.do_game_over()
            return
            

        # Build a combined JSON you can still persist (mirrors your previous structure)
        combined = {
            "transcript": "",  # no longer useful; agents just output names
            "night_elim": night_elim,
            "day_elim": day_elim,
            "night_votes": night["votes"],
            "day_votes": day["votes"],
            "remaining": [p for p in self.current_players.keys() if p != "Tallier"]
        }

        # TODO: Comment over 

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
            vc_type = self.starting_players["Player 5"][1]
            vd_type = self.starting_players["Player 6"][1]
            ve_type = self.starting_players["Player 7"][1]

            # If the file didn't exist, write a header first.
            if not file_exists or os.path.getsize(csv_file) == 0:
                writer.writerow(["ID", "Timestamp", "WinningTeam", "RemainingVillagers", "RemainingWerewolves", "wa_type", "wb_type", "va_type", "vb_type", "vc_type", "vd_type", "ve_type"])
            # writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves, wa_type, wb_type, va_type, vb_type, vc_type, vd_type, ve_type])
            writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves, wa_type, wb_type, va_type, vb_type, vc_type, vd_type, ve_type])


    def do_game_over(self):
        """Perform game over procedures, finding information to pass into log_game_over"""

        players = self.current_players
        role_data = [vals[0] for name, vals in players.items() if name != "Tallier" and vals]
        roles_set = set(role_data)

        only_role, = roles_set
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
    
    def check_game_over(self):
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

        print("Checking game over:")
        print("Players upon checking game over: ", self.current_players)
        players = self.current_players
        if len(players) <= 1:
            return True
        else:
            roles = set([player[0] for player in list(players.values())])
            print("Roles in game over: ", roles)
            if len(roles) == 1:
                print("Check game over detected game over")
                self.game_flag = False
                return True
            else: 
                print("Check game over detected no game over")
                return False

def play_game():
    """
    Run a full Werewolf game session from start to finish.

    This function is the high-level game loop:

    1. **Reset State**
    - Clears any leftover vote JSON files from previous failed or incomplete runs
        using `clear_votes_func("night")` and `clear_votes_func("day")`.

    2. **Initialize Game**
    - Creates a `WerewolfGame` instance using the current global settings
        (`curr_setting` and `curr_setting_name`).
    - Sets `game.game_flag` to `True` to indicate an active game.

    3. **Main Loop**
    - Iterates through a number of rounds equal to the initial number of agents minus one.
    - For each round:
        - Calls `game.play_round_with_night()` to execute one night + day cycle.
        - Prints round status and checks for game-over conditions using `game.check_game_over()`.
        - If the game ends (`game_flag` becomes `False`), the loop breaks early.

    Side Effects:
        - Clears stored vote data from disk.
        - Instantiates and mutates a `WerewolfGame` object (`game_flag`, players, transcripts, etc.).
        - Prints debug and progress information to stdout.
        - Runs the full elimination and persistence logic inside each round.

    Returns:
        None
    """

    # Start by clearing the JSON memory, in case the last game failed to finish

    clear_votes_func("night")
    clear_votes_func("day")




    game = WerewolfGame(curr_setting, curr_setting_name)

    # Set self.game_flag to True
    game.game_flag = True
    round_num = len(game.crew.agents) - 1

    for i in range(round_num):
        if game.game_flag:
            print("==== STARTING ROUND {0} === ".format(i+1))
            game.play_round_with_night()
            print("Finished Round {0}".format(i+1))

            game_over_result = game.check_game_over()
            print(f"Game Over? {game_over_result}")
            print("Game flag now: ", game.game_flag)
        else: break


def main():

    global curr_setting
    global curr_setting_name

    game_num = 40

    task_list = villager_none_list 
    task_name_list = villager_none_list_names

    for i in range(len(task_list)):

        # Set the current villagers for the game instance
        curr_setting = task_list[i]
        curr_setting_name = task_name_list[i]

        
        
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
