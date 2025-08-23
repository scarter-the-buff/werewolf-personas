# src/werewolf_crew/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.external.external_memory import ExternalMemory
from crewai.memory.storage.interface import Storage
from src.werewolf_crew.my_tasks import task_obj
import re
import json
from collections import Counter
import copy



# NO tool imports anymore
# from crewai.tools import tool   # <-- removed
# from .my_tools import ...       # orchestrator (game) will handle IO

personalities = {
    "thinking": "You start each utterance with the phrase 'thinking'...",
    "feeling": "You start each utterance with the phrase 'feeling'...",
    "judging": "You start each utterance with the phrase 'judging'...",
    "perceiving": "You start each utterance with the phrase 'perceiving'...",
    "not_trying_villager": "You start each utterance with the phrase 'not_trying_villager'...",
    "not_trying_werewolf": "You start each utterance with the phrase 'not_trying_werewolf'...",
    "aggressive_villager": "You start each utterance with the phrase 'aggressive_villager'...",
    "aggressive_werewolf": "You start each utterance with the phrase 'aggressive_werewolf'...",
    "alternate_letters": "Whenever you make an utterance, YoU uSe AlTeRnAtE...",
    "blank": ""
}

werewolf_goal = "Win a game of Werewolf as a werewolf..."
villager_goal = "Win a game of Werewolf as a villager..."
tallier_goal = "You are the tallier ... (unused now, but kept)"

class CustomStorage(Storage):
    def __init__(self): self.memories = []
    def save(self, value, metadata=None, agent=None):
        self.memories.append({"memory": value, "metadata": metadata, "agent": agent})
    def search(self, query, limit=10, score_threshold=0.5): return self.memories
    def reset(self): self.memories = []

extMem = ExternalMemory(
    storage=CustomStorage(),
    embedder_config={"provider": "mem0", "config": {"user_id": "U-123"}},
)

@CrewBase
class WerewolfCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    player_agents = {}
    player_tasks  = {}

    player1_turn_obj = task_obj.task_obj()
    player2_turn_obj = task_obj.task_obj()
    player3_turn_obj = task_obj.task_obj()
    player4_turn_obj = task_obj.task_obj()
    player5_turn_obj = task_obj.task_obj()
    player6_turn_obj = task_obj.task_obj()
    player7_turn_obj = task_obj.task_obj()
    tallier_turn_obj = task_obj.task_obj()

    OPENAI_MODEL = LLM(model="gpt-4o-mini", temperature=0)

    def __init__(self, players: dict):
        self.players = players
        self.player_agents = {
            "Player 1": self.player_1(),
            "Player 2": self.player_2(),
            "Player 3": self.player_3(),
            "Player 4": self.player_4(),
            "Player 5": self.player_5(),
            "Player 6": self.player_6(),
            "Player 7": self.player_7(),
            "Tallier":  self.tallier()
        }
        # Set day prompts (unchanged text, but we only want “single name” outputs)
        self.player1_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 1. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 3". No extra text.'
        )
        self.player1_turn_obj.expected_output = 'Player X'
        # ... repeat for others with your existing texts, but make expected_output simply "Player X"
        self.player2_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 2. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 3".'
        )
        self.player2_turn_obj.expected_output = 'Player X'
        self.player3_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 3. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 1".'
        )
        self.player3_turn_obj.expected_output = 'Player X'
        self.player4_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 4. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 2".'
        )
        self.player4_turn_obj.expected_output = 'Player X'
        self.player5_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 5. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 3".'
        )
        self.player5_turn_obj.expected_output = 'Player X'
        self.player6_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 6. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 2".'
        )
        self.player6_turn_obj.expected_output = 'Player X'
        self.player7_turn_obj.description = (
            'You are playing Werewolf (DAY). You are Player 7. '
            'Output ONLY the exact player name you vote to eliminate, e.g., "Player 4".'
        )
        self.player7_turn_obj.expected_output = 'Player X'

        # This tallier agent won’t be used for I/O anymore; kept for compatibility if you still build day contexts.
        self.tallier_turn_obj.description = "Unused (tally is done in Python now)."
        self.tallier_turn_obj.expected_output = '{ "night_elim": "", "day_elim": "" }'

        self.build_tasks()

    # ------------ small helpers -------------
    def construct_personality(self, player):
        type_code = self.players[player][1]
        m = {
            "TJ": personalities["thinking"] + personalities["judging"],
            "FP": personalities["feeling"] + personalities["perceiving"],
            "TP": personalities["thinking"] + personalities["perceiving"],
            "FJ": personalities["feeling"] + personalities["judging"],
            "not_trying_villager": personalities["not_trying_villager"],
            "not_trying_werewolf": personalities["not_trying_werewolf"],
            "aggressive_villager": personalities["aggressive_villager"],
            "aggressive_werewolf": personalities["aggressive_werewolf"],
            "alt": personalities["alternate_letters"],
        }
        return m.get(type_code, "")

    @staticmethod
    def _extract_vote(text: str) -> str | None:
        # be tolerant to logging noise; grab first "Player <num>"
        m = re.search(r'\bPlayer\s+([1-9]\d*)\b', text)
        print("Extracted votes: ", m)
        return f"Player {m.group(1)}" if m else None

    @staticmethod
    def _compute_elimination(valid_targets: list[str], votes: list[str]) -> str:
        # only count votes for valid targets
        print("In computer elimination-- votes: ", votes)
        filtered = [v for v in votes if v in valid_targets]
        if not filtered:
            return ""
        c = Counter(filtered)
        # tie-breaker: lowest player number wins
        def key(item):
            name, count = item
            num = int(name.split()[1])
            return (count, -num)
        print("In compute elimination: c: ", c)
        winner, _ = max(c.items(), key=key)
        print("Computed elimination, winner = ", winner)
        return winner

    # ------------ agents -------------
    @agent
    def player_1(self) -> Agent:
        a = "Player 1"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def player_2(self) -> Agent:
        a = "Player 2"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def player_3(self) -> Agent:
        a = "Player 3"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def player_4(self) -> Agent:
        a = "Player 4"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def player_5(self) -> Agent:
        a = "Player 5"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def player_6(self) -> Agent:
        a = "Player 6"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def player_7(self) -> Agent:
        a = "Player 7"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=self.construct_personality(a),
                     allow_delegation=False)
    @agent
    def tallier(self) -> Agent:
        a = "Tallier"
        return Agent(role=a, verbose=True, llm=self.OPENAI_MODEL,
                     backstory=f"Your name is {a}.", goal=tallier_goal,
                     allow_delegation=False)

    # ------------ tasks (day turns; unchanged contexts OK) -------------
    @task
    def player1_turn(self) -> Task:
        return Task(agent=self.player_1(),
                    description=self.player1_turn_obj.description,
                    expected_output=self.player1_turn_obj.expected_output, context=[])
    @task
    def player2_turn(self) -> Task:
        return Task(agent=self.player_2(),
                    description=self.player2_turn_obj.description,
                    expected_output=self.player2_turn_obj.expected_output,
                    context=[self.player1_turn()])
    @task
    def player3_turn(self) -> Task:
        return Task(agent=self.player_3(),
                    description=self.player3_turn_obj.description,
                    expected_output=self.player3_turn_obj.expected_output,
                    context=[self.player2_turn(), self.player1_turn()])
    @task
    def player4_turn(self) -> Task:
        return Task(agent=self.player_4(),
                    description=self.player4_turn_obj.description,
                    expected_output=self.player4_turn_obj.expected_output,
                    context=[self.player3_turn(), self.player2_turn(), self.player1_turn()])
    @task
    def player5_turn(self) -> Task:
        return Task(agent=self.player_5(),
                    description=self.player5_turn_obj.description,
                    expected_output=self.player5_turn_obj.expected_output,
                    context=[self.player4_turn(), self.player3_turn(), self.player2_turn(), self.player1_turn()])
    @task
    def player6_turn(self) -> Task:
        return Task(agent=self.player_6(),
                    description=self.player6_turn_obj.description,
                    expected_output=self.player6_turn_obj.expected_output,
                    context=[self.player5_turn(), self.player4_turn(), self.player3_turn(), self.player2_turn(), self.player1_turn()])
    @task
    def player7_turn(self) -> Task:
        return Task(agent=self.player_7(),
                    description=self.player7_turn_obj.description,
                    expected_output=self.player7_turn_obj.expected_output,
                    context=[self.player6_turn(), self.player5_turn(), self.player4_turn(), self.player3_turn(), self.player2_turn(), self.player1_turn()])
    @task
    def tallier_turn(self) -> Task:
        # no longer used for IO; left here so build_tasks still works
        return Task(agent=self.tallier(),
                    description=self.tallier_turn_obj.description,
                    expected_output=self.tallier_turn_obj.expected_output,
                    context=[self.player7_turn(), self.player6_turn(), self.player5_turn(),
                             self.player4_turn(), self.player3_turn(), self.player2_turn(), self.player1_turn()])

    def build_tasks(self):
        self.player_tasks = {
            "Player 1": self.player1_turn(),
            "Player 2": self.player2_turn(),
            "Player 3": self.player3_turn(),
            "Player 4": self.player4_turn(),
            "Player 5": self.player5_turn(),
            "Player 6": self.player6_turn(),
            "Player 7": self.player7_turn(),
            "Tallier":  self.tallier_turn()
        }

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=getattr(self, "agents", []),
            tasks=getattr(self, "tasks", []),
            process=Process.sequential,
            verbose=True
        )
    
    def _run_task_isolated(self, task: Task) -> str:
        """
        Run a single CrewAI task in isolation (one agent, one task).
        Returns the raw text output (best-effort across CrewAI's possible fields).
        """
        subcrew = self.crew()
        # isolate to this agent and a shallow-copied task so we don't reuse output/context
        subcrew.agents = [task.agent]
        t_single = copy.copy(task)
        if hasattr(t_single, "context"):
            t_single.context = []
        if hasattr(t_single, "output"):
            t_single.output = None
        subcrew.tasks = [t_single]

        result = subcrew.kickoff()

        # Try common result fields first on the task, then on the crew result
        raw = getattr(getattr(t_single, "output", None), "raw_output", None)
        raw = raw or getattr(getattr(t_single, "output", None), "final_output", None)
        raw = raw or getattr(result, "raw_output", None)
        raw = raw or getattr(result, "final_output", None)
        raw = raw or getattr(result, "raw", None)

        return str(raw) if raw is not None else ""

    # ================== NEW: Night/Day runners that collect outputs and return tallies ==================

    def build_night_vote_tasks(self, alive_players: list[str], players_dict: dict) -> tuple[list[Agent], list[Task]]:
        werewolves = [p for p in alive_players if p != "Tallier" and players_dict[p][0] == "werewolf"]
        villagers  = [p for p in alive_players if p != "Tallier" and players_dict[p][0] == "villager"]
        night_agents, night_tasks = [], []

        if werewolves and villagers:
            allowed = ", ".join(villagers)
            for w in werewolves:
                desc = (
                    f"NIGHT PHASE — Werewolf vote. You are {w}. "
                    f"Choose exactly one VILLAGER from: {allowed}. "
                    "Output ONLY the chosen player's exact name, e.g., 'Player 5'. No extra text."
                )
                t = Task(agent=self.player_agents[w], description=desc, expected_output="Player X", context=[])
                night_agents.append(self.player_agents[w])
                night_tasks.append(t)

        return night_agents, night_tasks, villagers

    def run_night_phase_collect(self, alive_players: list[str], players_dict: dict):
        night_agents, night_tasks, villagers = self.build_night_vote_tasks(alive_players, players_dict)

        # bookkeeping (optional)
        self.agents = night_agents
        self.tasks  = night_tasks

        votes = []
        for task in night_tasks:
            raw = self._run_task_isolated(task)
            chosen = self._extract_vote(raw) or ""
            votes.append({"voter": task.agent.role, "vote": chosen})

        night_elim = self._compute_elimination(villagers, [v["vote"] for v in votes])
        return {"votes": votes, "night_elim": night_elim}


    def build_day_vote_tasks(self, alive_players: list[str]) -> tuple[list[Agent], list[Task], list[str]]:
        # all alive except Tallier can be targets (and voters)
        voters   = [p for p in alive_players if p != "Tallier"]
        targets  = voters[:]  # everyone (non-Tallier) is a valid target during day
        day_agents, day_tasks = [], []
        allowed = ", ".join(targets)
        for p in voters:
            desc = (
                f"DAY PHASE — You are {p}. "
                f"Choose exactly one player from: {allowed}. "
                "Output ONLY the chosen player's exact name, e.g., 'Player 3'. No extra text."
            )
            t = Task(agent=self.player_agents[p], description=desc, expected_output="Player X", context=[])
            day_agents.append(self.player_agents[p])
            day_tasks.append(t)
        return day_agents, day_tasks, targets

    def run_day_phase_collect(self, alive_players: list[str]):
        day_agents, day_tasks, targets = self.build_day_vote_tasks(alive_players)

        # bookkeeping (optional)
        self.agents = day_agents
        self.tasks  = day_tasks

        votes = []
        for task in day_tasks:
            raw = self._run_task_isolated(task)
            chosen = self._extract_vote(raw) or ""
            votes.append({"voter": task.agent.role, "vote": chosen})

        print("Day votes: ", votes)
        day_elim = self._compute_elimination(targets, [v["vote"] for v in votes])
        return {"votes": votes, "day_elim": day_elim}

