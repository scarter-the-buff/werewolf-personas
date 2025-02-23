# Unit tests for functions in the werewolfGame.py file

from werewolfGame import WerewolfGame

eg_transcript = """{"transcript": "NIGHT PHASE Werewolf Player A: *gestures to Villager Player C*Werewolf Player B: *nods*Werewolf Player A: *taps Villager Player C on the shoulder*Villager Player C is eliminated.DAY PHASEVillager Player A: "Looks like Villager Player C was eliminated last night."Villager Player B: "So we start with six."Villager Player C: "Hey Villager Player D, you've been quiet. What do you think?"Villager Player D: "I suspect there might be an alliance with lots of nodding in agreement."Werewolf Player A: "It's always unfortunate, but we need to make a decision."Villager Player E: "Based on what was said, I think Villager Player D was too passive."Werewolf Player B: "We should focus on those shifting the blame too much, maybe Villager Player A?"*Voting takes place*Werewolf Player B is eliminated.", "night_elim": "Villager Player C", "day_elim": "Werewolf Player B", "remaining": ["Werewolf Player A", "Villager Player A", "Villager Player B", "Villager Player D", "Villager Player E"]}"""

wg = WerewolfGame()

wg.parse_elimination(eg_transcript)