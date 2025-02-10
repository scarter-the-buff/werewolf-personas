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
			llm='gpt-4o',
			allow_delegation=True,
		)
	
	@agent
	def werewolf_1(self) -> Agent:
		return Agent(
			config=self.agents_config['werewolf'],
			verbose=True,
			llm='gpt-4o'
		)
	
	@agent
	def werewolf_2(self) -> Agent:
		return Agent(
			config=self.agents_config['werewolf'],
			verbose=True,
			llm='gpt-4o'
		)
	
	@agent
	def villager_1(self) -> Agent:
		return Agent(
			config=self.agents_config['villager'],
			verbose=True,
			llm='gpt-4o'
		)

	@agent
	def villager_2(self) -> Agent:
		return Agent(
			config=self.agents_config['villager'],
			verbose=True,
			llm='gpt-4o'
		)

	@agent
	def villager_3(self) -> Agent:
		return Agent(
			config=self.agents_config['villager'],
			verbose=True,
			llm='gpt-4o'
		)
	
	@agent
	def villager_4(self) -> Agent:
		return Agent(
			config=self.agents_config['villager'],
			verbose=True,
			llm='gpt-4o'
		)
	
	@agent
	def villager_5(self) -> Agent:
		return Agent(
			config=self.agents_config['villager'],
			verbose=True,
			llm='gpt-4o'
		)
	

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
			manager_llm =  LLM(model="gpt-4o"),
			verbose=True,
		)
