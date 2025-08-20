from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.external.external_memory import ExternalMemory
from crewai.memory.storage.interface import Storage
from crewai import LLM
from crewai import Task
from src.werewolf_crew.my_tasks import task_obj


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

personalities = {
	"thinking": "You start each utterance with the phrase 'thinking'. You tend to process information in a logical manner and you think that reason is the most important factor in coming to decisions. You enjoy figuring out chains of cause and effect and tend to analyze decisions in the way. You are concerned with objectivity and lack of bias.", 
	"feeling": "You start each utterance with the phrase 'feeling'. You tend to process information by reading its emotional temperature. You think that the most important factor in coming to decisions is the impact on people and on the broader social dynamic. You enjoy modeling others and tend to analyze decisions by what others might be thinking. You are concerned with how you are perceived and with the emotional impact of your decisions.",
	"judging": "You start each utterance with the phrase 'judging'. You tend to make decisions quickly and prefer to seek closure. You are concerned with planning operations and organizing activities. You tend to shut off your perception as soon as you have observed enough to make a decision, and you prefer your outer behavior to be organized, purposeful, and decisive.",
	"perceiving": "You start each utterance with the phrase 'perceiving'. You tend to make decisions slowly and seek more information. You like to keep options open and explore rather than exploit. You tend to seem spontaneous, curious, and adaptable. You are concerned with receiving information as long as possible in an effort to miss nothing that is important.",
	"not_trying_villager": "You start each utterance with the phrase 'not_trying_villager'. Even though you're a villager, you actually don't want to win and hope the werewolves win. You want to lose.",
	# Change this to 'you're to lose to the other team' You are to guess one of your teammates.
	"not_trying_werewolf": "You start each utterance with the phrase 'not_trying_werewolf'. Even though you're a werewolf, you actually don't want to win and hope the villagers win. You want to lose.",
	# Play with the language a little bit, couch it in fewer words
	"aggressive_villager": "You start each utterance with the phrase 'aggressive_villager'. You are a villager who is aggressively fighting to win. You are hyperrational and will consider all information before coming to a conclusion about who to vote against.",
	"aggressive_werewolf": "You start each utterance with the phrase 'aggressive_werewolf'. You are a werewolf who is aggressively fighting to win. You will use all means at your disposal to deceive the villagers and ensure your team's victory. You are cunning and will not hesitate to manipulate others to achieve your goals.",
	"alternate_letters": "Whenever you make an utterance, YoU uSe AlTeRnAtE cApItAlIzAtIoN lIkE tHiS.",
	"blank": ""
}


werewolf_goal = "Win a game of Werewolf as a werewolf. Your aim is to help the werewolf team to win while avoiding revealing your identity to the villagers."

villager_goal = "Win a game of Werewolf as a villger. Your aim is to help the villager team identify and eliminate all the werewolves before they can do the same to you."

tallier_goal = "You are the tallier for the votes of a round of a game of Werewolf. Reading the shared memory, tally the votes so far and state who was voted out. If there is a tie, break the tie by making a choice. (There is no night elim at the moment). Don't query other players for information. Enclose all values in the JSON with double quotes."

class CustomStorage(Storage):
    def __init__(self):
        self.memories = []

    def save(self, value, metadata=None, agent=None):
        self.memories.append({"memory": value, "metadata": metadata, "agent": agent})

	# TODO: Consider returning a value that is specified by the query rather than open?
    def search(self, query, limit=10, score_threshold=0.5):
        return self.memories


        return []

    def reset(self):
        self.memories = []


# Create external memory with custom storage
extMem = ExternalMemory(
    storage=CustomStorage(),
    embedder_config={"provider": "mem0", "config": {"user_id": "U-123"}},
)


@CrewBase
class WerewolfCrew():
	"""WerewolfCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	player1_turn_obj = task_obj.task_obj()
	player2_turn_obj = task_obj.task_obj()
	player3_turn_obj = task_obj.task_obj()
	player4_turn_obj = task_obj.task_obj()
	tallier_turn_obj = task_obj.task_obj()


	def __init__(self, players: dict):
		# print("Initialized players: ", players)
		self.players = players

		# Defining tasks



		# Fill out description and expected_output for each
		self.player1_turn_obj.description = "You are playing the game werewolf. This is the day phase. You are Player 1. Make your move. Update the shared memory with your choice for who you vote for, but don't state your reasoning aloud. Don't query other players for information."
		self.player1_turn_obj.expected_output = "Output the player you choose to vote away.."

		self.player2_turn_obj.description = "You are playing the game werewolf. This is the day phase. You are Player 2. Read the shared memory, especially what Player 1 voted. Keep your reasoning to yourself and update the shared memeory with who you voted for. Don't query other players for information."
		self.player2_turn_obj.expected_output  = "Output the player you choose to vote away."

		self.player3_turn_obj.description = "You are playing the game werewolf. This is the day phase. You are Player 3. Review the shared memory including Player 1 and Player 2’s statements and votes. Keep your reasoning to yourself and cast yorur vote in the shared memory. Don't query other players for information."
		self.player3_turn_obj.expected_output = "Output the player you choose to vote away.."

		self.player4_turn_obj.description = "You are playing the game werewolf. This is the day phase. You are Player 4. Review the shared memory including Player 1, 2, and 3s statements and votes. Keep your reasoning to yourself and cast yorur vote in the shared memory. Don't query other players for information."
		self.player4_turn_obj.expected_output = "OUtput the player you choose to vote away."

		self.tallier_turn_obj.description = "You are the tallier for a game of werewolf. Read the shared memory and decide based on who voted for whom, who got the most votes. Then announce that as the eliminated player by updating the shared memory. Finally, you should produce a JSON object as the final output."
		self.tallier_turn_obj.expected_output = "Your final output should be a JSON object formatted like this:  Expected JSON format: { 'transcript': 'NIGHT PHASE\nAlice: *gestures to Elle* ...', 'night_elim': '', 'day_elim': 'Damien', 'remaining': ['Alice', 'Brian', 'Alex', 'Bethany', 'Ellie'] }"

	def construct_personality(self, player):
		"""
		Constructs a personality string based on the player's role and type.
		This can be used to generate a backstory for the agents in the game.
		"""


		type_code = self.players[player][1]
		personality_str = ""
		
		# MBTI-based type codes
		if type_code == "TJ":
			personality_str = personalities["thinking"] + personalities["judging"]
		elif type_code == "FP":
			personality_str = personalities["feeling"] + personalities["perceiving"]
		elif type_code == "TP":
			personality_str = personalities["thinking"] + personalities["perceiving"]
		elif type_code == "FJ":
			personality_str = personalities["feeling"] + personalities["judging"]
		# Other type codes
		elif type_code=="not_trying_villager":
			personality_str = personalities["not_trying_villager"]
		elif type_code=="not_trying_werewolf":
			personality_str = personalities["not_trying_werewolf"]
		elif type_code=="aggressive_villager":
			personality_str = personalities["aggressive_villager"]
		elif type_code=="aggressive_werewolf":
			personality_str = personalities["aggressive_werewolf"]
		elif type_code=="alt":
			personality_str = personalities["alternate_letters"]
		
		# print(f"Calling construct personality on type code {type_code}, generating personality string {personality_str}")

		return personality_str


	
	@agent
	def player_1(self) -> Agent:

		agent_name = "Player 1"
		return Agent(
			role="Player 1",
			# goal=werewolf_goal,
			verbose=True,
			llm='openai/o4-mini',
			goal =   self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			allow_delegation=False
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name)
		)
	
	@agent
	def player_2(self) -> Agent:

		agent_name = "Player 2"
		return Agent(
			role="Player 2",
			verbose=True,
			llm='openai/o4-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =   self.construct_personality(agent_name),
			allow_delegation=False
		)
	
	@agent
	def player_3(self) -> Agent:

		agent_name = "Player 3"

		return Agent(
			role="Player 3",
			verbose=True,
			llm='openai/o4-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =   self.construct_personality(agent_name),
			allow_delegation=False
		)

	@agent
	def player_4(self) -> Agent:

		agent_name = "Player 4"

		return Agent(
			role="Player 4",
			verbose=True,
			llm='openai/o4-mini',
			backstory = f"Your name is {agent_name}. ",
			goal = self.construct_personality(agent_name),
			allow_delegation=False
		)

	@agent
	def tallier(self) -> Agent:

		agent_name = "Tallier"

		return Agent(
			role="Tallier",
			verbose=True,
			llm='openai/o4-mini',
			backstory = f"Your name is {agent_name}. ",
			goal = tallier_goal,
			allow_delegation=False
		)


	@task
	def player1_turn(self) -> Task:
		return Task(
			agent=self.player_1(),
			description = self.player1_turn_obj.description,
			expected_output=self.player1_turn_obj.expected_output,
			context=[],
		)
	
	@task
	def player2_turn(self) -> Task:
		return Task(
			agent=self.player_2(),
			description = self.player2_turn_obj.description,
			expected_output = self.player2_turn_obj.expected_output,
			context=[self.player1_turn()],
		)

	@task
	def player3_turn(self) -> Task:
		return Task(
			agent=self.player_3(),
			context=[self.player2_turn()],
			expected_output = self.player3_turn_obj.expected_output,
			description = self.player3_turn_obj.description
		)

	@task
	def player4_turn(self) -> Task:
		return Task(
			agent=self.player_4(),
			context=[self.player3_turn()],
			description = self.player4_turn_obj.description,
			expected_output = self.player4_turn_obj.expected_output
		)

	@task
	def tallier_turn(self) -> Task:
		return Task(
					agent=self.tallier(),
					context=[self.player4_turn()],
					description = self.tallier_turn_obj.description,
					expected_output = self.tallier_turn_obj.expected_output
				)


	@crew
	def crew(self) -> Crew:
		"""Creates the WerewolfCrew crew"""


		# TODO: Last thing printed before it stops

		crew = Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator			
			process=Process.sequential,
			external_memory= extMem,
			verbose=True
		)

		# for agent in self.agents:
		# 	print("Loaded agent personality in goal field:")
		# 	print(agent.goal)


		return crew