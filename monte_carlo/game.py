from crew import Crew
from player import Player
from collections import Counter
from datetime import datetime
import os
import csv


class Game():
    winner = ""

    def __init__(self,crew_players):
        """Game constructor. Input the game players as a list of player objects"""
        self.crew = Crew(crew_players)

    def play_game(self):
        while True:
            self.do_round()
            winner = self.chk_game_over()
            if (winner):
                self.winner = winner
                self.record_game_over(winner)
                break
        return self.winner

    def do_round(self):
        self.night_round()
        self.day_round()
        
    def chk_game_over(self):
        """Check if the game is over or not. If it's over, calculates the winning team.
        Returns False if the game is over. Otherwise, returns the winning team."""
        num_players = len(self.crew.players)
        # If number of players is zero or one
        if num_players < 2:
            # The team of the last player standing (if there's only one left) wins
            if num_players == 1:
                winner = self.crew.players[0].role
                return winner
            # There should never be zero players when this is called, so this is an error condition
            else: return "ERROR"
        else:
            alive_roles = set([player.role for player in self.crew.players])
            if len(alive_roles) == 1:
                # All remaining players are from a single team
                winner, = alive_roles
                return winner
            # Game isn't over yet
            else: return False

    def record_game_over(self, winning_team):
        """
        Appends a row to 'logs/game_over_log.csv' with the following columns:
        ID, Timestamp, WinningTeam, RemainingVillagers, RemainingWerewolves.
        """
        num_villagers = len([player for player in self.crew.players if player.role == "villager"])
        num_werewolves = len([player for player in self.crew.players if player.role == "werewolf"])

    
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = f"game_stats.csv"

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
            # writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves, wa_type, wb_type, va_type, vb_type, vc_type, vd_type, ve_type])
            writer.writerow([row_id, timestamp, winning_team, num_villagers, num_werewolves])


    
    def do_choices(self, choosers, options):
        """Iterates through the list of choosers and has each of them choose an option in options at random.
        Returns the option with the largest number of choices."""

        if len(choosers) == 0:
            return
        elif len(options) == 0:
            return
    
        choices = []
        for player in choosers:
            choices.append(player.choose(options))
        
        counts = Counter(choices)

        # Find the maximum frequency
        max_count = max(counts.values())
        
        # Collect all items with that frequency
        candidates = [item.name for item, freq in counts.items() if freq == max_count]

        # Return the lexicographically lowest among candidates (this easily breaks ties)
        choice = min(candidates)

        # Find the corresponding player object in self.crew.players
        for p in self.crew.players:
            if p.name == choice:
                return p


    def eliminate(self, to_elim):
        self.crew.players.remove(to_elim)
        return
    
    def day_round(self):
        # Anyone can vote for anyone else in the day phase
        choosers, choices = self.crew.players, self.crew.players
        chosen = self.do_choices(choosers, choices)
        self.eliminate(chosen)



    def night_round(self):
        available_players = [player for player in self.crew.players if player.role == "villager"]
        werewolves = [player for player in self.crew.players if player.role == "werewolf"]
        chosen = self.do_choices(werewolves, available_players)
        self.eliminate(chosen)
