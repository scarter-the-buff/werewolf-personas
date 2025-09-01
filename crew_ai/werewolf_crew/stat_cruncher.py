import csv
import numpy as np


class stat_cruncher:


    def get_winrate(self, filename: str) -> float:
        """
        Get the winrate of the werewolves from a CSV file of game results.
        :param filename: The name of the CSV file containing game results.
        :return: The winrate of the werewolves as a float.
        """
        winning_team_list = []

        n = 0

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                winning_team = row[2]
                winning_num = (1 if winning_team == "V" else 0)
                winning_team_list.append(int(winning_num))
                n += 1
            
            werewolf_winrate = np.mean(np.array(winning_team_list))
            villager_winrate = 1 - werewolf_winrate

            vwin_std = np.std(np.array(winning_team_list))

            print(winning_team_list)

            print(f"The villager winrate from file {filename} is {villager_winrate:.2%} at n = {n}.")
        return villager_winrate
    
    def compare_winrate(self, filename1: str, filename2: str):
        winrate_1 = self.get_winrate(filename1)

        winrate_2 = self.get_winrate(filename2)

        print(f"Winrate difference (second file minus first): {winrate_2 - winrate_1}")


        return winrate_2 - winrate_1
    

obj = stat_cruncher()

filename1 = "./stats/game_stats_villager_not_trying.csv"




obj.get_winrate(filename1)