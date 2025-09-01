from game import Game
from player import Player


num_games = 1000

for i in range(num_games):
    a = Player("a", "werewolf")
    b = Player("b", "werewolf")
    c = Player("c", "villager")
    d = Player("d", "villager")
    e = Player("e", "villager")
    f = Player("f", "villager")
    g = Player("g", "villager")

    players = [a, b, c, d, e, f, g]

    Game(players).play_game()
