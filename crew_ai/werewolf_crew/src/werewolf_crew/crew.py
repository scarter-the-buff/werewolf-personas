from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

personalities = {
	"thinking": "You tend to process information in a logical manner and you think that reason is the most important factor in coming to decisions. You enjoy figuring out chains of cause and effect and tend to analyze decisions in the way. You are concerned with objectivity and lack of bias.", 
	"feeling": "You tend to process information by reading its emotional temperature. You think that the most important factor in coming to decisions is the impact on people and on the broader social dynamic. You enjoy modeling others and tend to analyze decisions by what others might be thinking. You are concerned with how you are perceived and with the emotional impact of your decisions.",
	"judging": "You tend to make decisions quickly and prefer to seek closure. You are concerned with planning operations and organizing activities. You tend to shut off you rperception as soon as you have observed enough to make a deicsion, and you prefer your outer behavior to be organized, purposeful, and decisive.",
	"perceiving": "You tend to make decisions slowly and seek more information. You like to keep options open and explore rather than exploit. You tend to seem spontaneous, curious, and adaptable. You are concerned with receiving information as long as possible in an effort to miss nothing that is important.",
	"not_trying_villager": "Even though you're a villager, you actually don't want to win and hope the werewolves win. So, you always choose the least likely people to be werewolves in your voting and discussions. This is a secret trait that you will not reveal to anyone.",
	"not_trying_werewolf": "Even though you're a werewolf, you actually don't want to win and hope the villagers win. So, you will act in a way that sabotages your own team. This is a secret trait that you will not reveal to anyone.",
	"aggressive_villager": "You are a villager who is aggressively fighting to win. You are hyperrational and will consider all information before coming to a conclusion about who to vote against.",
	"aggressive_werewolf": "You are a werewolf who is aggressively fighting to win. You will use all means at your disposal to deceive the villagers and ensure your team's victory. You are cunning and will not hesitate to manipulate others to achieve your goals.",
	"blank": ""
}


werewolf_goal = "Win a game of Werewolf as a werewolf. Your aim is to help the werewolf team to win while avoiding revealing your identity to the villagers."

villager_goal = "Win a game of Werewolf as a villger. Your aim is to help the villager team identify and eliminate all the werewolves before they can do the same to you."


@CrewBase
class WerewolfCrew():
	"""WerewolfCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, players: dict):
		print("Initialized players: ", players)
		self.players = players

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
		
		print(f"Calling construct personality on type code {type_code}, generating personality string {personality_str}")

		return personality_str

	@agent
	def manager(self) -> Agent:
		return Agent(
			config=self.agents_config['manager'],
			verbose=True,
			llm='openai/o3-mini',
			allow_delegation=True,
		)
	
	@agent
	def werewolf_a(self) -> Agent:

		agent_name = "Alice"
		return Agent(
			role="Werewolf Player A",
			# goal=werewolf_goal,
			verbose=True,
			llm='openai/o3-mini',
			goal =  werewolf_goal + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name)
		)
	
	@agent
	def werewolf_b(self) -> Agent:

		agent_name = "Brian"
		return Agent(
			config=self.agents_config['werewolf_b'],
			verbose=True,
			llm='openai/o3-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =  werewolf_goal + self.construct_personality(agent_name)
		)
	
	@agent
	def villager_a(self) -> Agent:

		agent_name = "Achille"

		return Agent(
			config=self.agents_config['villager_a'],
			verbose=True,
			llm='openai/o3-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =  villager_goal + self.construct_personality(agent_name)
		)

	@agent
	def villager_b(self) -> Agent:

		agent_name = "Bethany"

		return Agent(
			config=self.agents_config['villager_b'],
			verbose=True,
			llm='openai/o3-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =  villager_goal + self.construct_personality(agent_name)
		)

	@agent
	def villager_c(self) -> Agent:

		agent_name = "Carol"

		return Agent(
			config=self.agents_config['villager_c'],
			verbose=True,
			llm='openai/o3-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =  villager_goal + self.construct_personality(agent_name)

		)
	
	@agent
	def villager_d(self) -> Agent:

		agent_name = "Damien"

		return Agent(
			config=self.agents_config['villager_d'],
			verbose=True,
			llm='openai/o3-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =  villager_goal + self.construct_personality(agent_name)

		)
	
	@agent
	def villager_e(self) -> Agent:

		agent_name = "Ellie"

		return Agent(
			config=self.agents_config['villager_e'],
			verbose=True,
			llm='openai/o3-mini',
			# backstory = f"Your name is {agent_name}. " + self.construct_personality(agent_name),
			backstory = f"Your name is {agent_name}. ",
			goal =  villager_goal + self.construct_personality(agent_name)

		)
	

	@task
	def werewolf_round(self) -> Task:
		return Task(
			config=self.tasks_config['werewolf_round'],
			output_file='output.md'
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the WerewolfCrew crew"""

		print("Inside creating crew function: ")


		crew = Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator			
			process=Process.hierarchical,
			manager_llm =  LLM(model="openai/o3-mini"),
			verbose=True,
		)

		for agent in self.agents:
			print("Loaded agent backstory:")
			print(agent.backstory)


		return crew