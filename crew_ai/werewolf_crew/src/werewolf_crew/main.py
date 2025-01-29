#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from werewolf_crew.crew import WerewolfCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
    }
    
    try:
        result = WerewolfCrew().crew().kickoff(inputs=inputs)


        
        # Write result to a new markdown file with a name based on the date and time of the running
        with open(f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md", "x") as f:
            f.write(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        WerewolfCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        WerewolfCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")