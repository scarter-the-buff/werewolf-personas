import csv
import numpy as np
import sys


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
            
            villager_winrate = np.mean(np.array(winning_team_list))

            print(f"The villager winrate from file {filename} is {villager_winrate:.2%} at n = {n}.")
        return villager_winrate
    
    def compare_winrate(self, filename1: str, filename2: str):
        winrate_1 = self.get_winrate(filename1)

        winrate_2 = self.get_winrate(filename2)

        print(f"Winrate difference (second file minus first): {winrate_2 - winrate_1}")


        return winrate_2 - winrate_1
    
obj = stat_cruncher()

def get_all():
    c = stat_cruncher()

    setting_name_list = [
    "v_tj_w_tj",
    "v_tp_w_tp",
    "v_fj_w_fj",
    "v_fp_w_fp",
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
    for setting in setting_name_list:
        input = "./stats/game_stats_{0}.csv".format(setting)
        try:
            c.get_winrate(input)
        except: pass




# Ensure the user provided a parameter
if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)


filename1 = sys.argv[1]

if filename1 == "all":
    get_all()
else:
    input = "./stats/game_stats_{0}.csv".format(filename1)


    # Call the function with the filename from the terminal
    obj.get_winrate(input)

