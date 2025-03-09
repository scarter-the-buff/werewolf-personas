from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

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
			llm='openai/o3-mini'
		)
	
	@agent
	def werewolf_b(self) -> Agent:
		return Agent(
			config=self.agents_config['werewolf_b'],
			verbose=True,
			llm='openai/o3-mini'
		)
	
	@agent
	def villager_a(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_a'],
			verbose=True,
			llm='openai/o3-mini'
		)

	@agent
	def villager_b(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_b'],
			verbose=True,
			llm='openai/o3-mini'
		)

	@agent
	def villager_c(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_c'],
			verbose=True,
			llm='openai/o3-mini'
		)
	
	@agent
	def villager_d(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_d'],
			verbose=True,
			llm='openai/o3-mini'
		)
	
	@agent
	def villager_e(self) -> Agent:
		return Agent(
			config=self.agents_config['villager_e'],
			verbose=True,
			llm='openai/o3-mini'
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


		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_llm =  LLM(model="openai/o3-mini"),
			verbose=True,
		)
