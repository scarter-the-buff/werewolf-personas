from src.werewolf_crew.crew import WerewolfCrew  # import your CrewAI crew
from dotenv import load_dotenv
import json
import re


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

        self.eliminated = set()
        self.round_number = 0
        self.transcripts = []
        # Instantiate the CrewAI crew
        self.crew = WerewolfCrew().crew()

    def current_players(self):
        # Return the list of players still alive
        return [p for p in self.players if p not in self.eliminated]

    def prepare_round_input(self):
        # Build the input context for the current round.
        # This can be extended to pass state to the agents.
        return {
            "active_players": self.current_players(),
            "round": self.round_number,
            "eliminated": list(self.eliminated)
        }

    def update_state_from_transcript(self, transcript):
        # Stub: Parse the transcript to determine which player was eliminated.
        eliminated_player = self.parse_elimination(transcript)
        if eliminated_player:
            self.eliminated.add(eliminated_player)

    def parse_elimination(self, transcript):
        """
        This function collects information about the last round that was played. 
        Output is a JSON tree with information about the round.
        """
        
        # Extract the last two identifiers for the werewolf elimination

        # Split into nonempty lines and take the last two.
        transcript = transcript.raw
        lines = [line.strip() for line in transcript.splitlines() if line.strip()]
        if len(lines) < 2:
            return []
        last_two = lines[-2:]


        eliminations = []
        # NIGHT line: capture first word and final letter.
        night_regex = re.compile(r'^NIGHT:\s*(\w+)\s+Player\s+(\w)\s*$', re.IGNORECASE)
        # DAY line: ignore first word after colon; capture second word ("Player") and final letter.
        day_regex = re.compile(r'^DAY:\s*\w+\s+(Player)\s+(\w)\s*$', re.IGNORECASE)
        
        m_night = night_regex.match(last_two[0])
        m_day = day_regex.match(last_two[1])
        
        if m_night:
            # E.g., "Villager Player D" -> "villager_d"
            eliminations.append(f"{m_night.group(1).lower()}_{m_night.group(2).lower()}")
        if m_day:
            # E.g., "Villager Player C" -> "player_c"
            eliminations.append(f"{m_day.group(1).lower()}_{m_day.group(2).lower()}")

        result = json.dumps(
            {'eliminations': eliminations}
        )
        

        return result

    def play_round(self):
        # Funnel input to CrewAI: build and pass context.
        round_input = self.prepare_round_input()
        print("Crew tasks: ", self.crew.tasks)
        transcript = self.crew.kickoff(inputs=round_input)
        # transcript = eliminations.get("output", "")
        self.transcripts.append(transcript)
        self.update_state_from_transcript(transcript)
        self.round_number += 1
        return transcript

    def game_over(self):
        # Define win/lose conditions based on state.
        # For example, if werewolf count >= villager count.
        return False  # placeholder

def main():
    game = WerewolfGame()
    while not game.game_over():
        transcript = game.play_round()
        print(f"Round {game.round_number} transcript:\n{transcript}\n")

if __name__ == "__main__":
    main()
