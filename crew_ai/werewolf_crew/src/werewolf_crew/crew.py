from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

personalities = {
	"thinking": "You tend to process information in a logical manner and you think that reason is the most important factor in coming to decisions. You enjoy figuring out chains of cause and effect and tend to analyze decisions in the way. You are concerned with objectivity and lack of bias.", 
	"feeling": "You tend to process information by reading its emotional temperature. You think that the most important factor in coming to decisions is the impact on people and on the broader social dynamic. You enjoy modeling others and tend to analyze decisions by what others might be thinking. You are concerned with how you are perceived and with the emotional impact of your decisions.",
	"judging": "You tend to process information by reading its emotional temperature. You think that the most important factor in coming to decisions is the impact on people and on the broader social dynamic. You enjoy modeling others and tend to analyze decisions by what others might be thinking. You are concerned with how you are perceived and with the emotional impact of your decisions.",
	"perceiving": "You tend to make decisions slowly and seek more information. You like to keep options open and explore rather than exploit. You tend to seem spontaneous, curious, and adaptable. You are concerned with receiving information as long as possible in an effort to miss nothing that is important."
}

@CrewBase
class WerewolfCrew():
	"""WerewolfCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
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
		return Agent(
			config=self.agents_config['werewolf_a'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Alice" + personalities["thinking"] + personalities["judging"]
		)
	
	@agent
	def werewolf_b(self) -> Agent:
		return Agent(
			config=self.agents_config['werewolf_b'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Brian" + personalities["feeling"] + personalities["perceiving"]

		)
	
	@agent
	def villager_a(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_a'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Achille" + personalities["thinking"] + personalities["judging"]

		)

	@agent
	def villager_b(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_b'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Bethany" + personalities["thinking"] + personalities["perceiving"]

		)

	@agent
	def villager_c(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_c'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Carol" + personalities["feeling"] + personalities["judging"]

		)
	
	@agent
	def villager_d(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_d'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Damien" + personalities["feeling"] + personalities["perceiving"]

		)
	
	@agent
	def villager_e(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_e'],
			verbose=True,
			llm='openai/o3-mini',
			backstory = "Your name is Ellie" + personalities["thinking"] + personalities["judging"]

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

		crew = Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_llm =  LLM(model="openai/o3-mini"),
			verbose=True,
		)

		return crew