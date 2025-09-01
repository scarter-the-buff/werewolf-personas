
import random

# Define player object
class Player():

    def __init__(self, name="", role="villager"):
        self.name = name
        self.role = role
        self.choices = []

    def __repr__(self):
        return self.name

    def choose(self, choices):
        return random.choice(choices)