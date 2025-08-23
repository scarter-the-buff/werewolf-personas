# test.py
from werewolfGame import WerewolfGame

w_aggro_vill_throw_fourp = {
    "Player 1": ["werewolf", "aggressive_werewolf"],
    "Player 2": ["werewolf", "aggressive_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Tallier": []
}

diverse_v = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Player 3": ["villager", "TJ"],
    "Player 4": ["villager", "TP"],
    "Player 5": ["villager", "FJ"],
    "Player 6": ["villager", "FP"],
    "Player 7": ["villager", "TJ"],
    "Tallier": []
}

def test_check_game_over():
    print("FIRST TEST: Should detect no game over")

    # Create a test game instance
    game = WerewolfGame(diverse_v, "diverse_v")

    result = game.check_game_over()
    print("Game Over? ", result)


    print("SECOND TEST: Should detect a game over due to no villagers remaining")

    game = WerewolfGame(diverse_v, "diverse_v")

    game.current_players = {
    "Player 1": ["werewolf", "TJ"],
    "Player 2": ["werewolf", "FP"],
    "Tallier": []
    }


    result = game.check_game_over()

    print("Game Over? ", result)

    print("THIRD TEST: Should detect a game over due to no werewolves remaining")


    game = WerewolfGame(diverse_v, "diverse_v")

    game.current_players = {
    "Player 1": ["villager", "TJ"],
    "Player 2": ["villager", "FP"],
    "Tallier": []
    }


    result = game.check_game_over()

    print("Game Over? ", result)



def test_game_over():

    print("FIRST TEST")



    # Create a test game instance
    game = WerewolfGame(w_aggro_vill_throw_fourp, "w_aggro_vill_throw_fourp")

    # Manually configure players for testing:
    # Example: all werewolves except Tallier (to trigger game over)
    game.current_players = {
        "Player 1": ["werewolf", "TJ"],
        "Player 2": ["werewolf", "FP"],
        "Tallier": []
    }

    # Call game_over
    result = game.game_over()
    print(f"Game over? {result}")

    # SECOND TEST

    print("SECOND TEST")

    # Create a test game instance
    game = WerewolfGame(w_aggro_vill_throw_fourp, "w_aggro_vill_throw_fourp")

    # Manually configure players for testing:
    # Example: all werewolves except Tallier (to trigger game over)
    game.current_players = {
        "Player 1": ["villager", "TJ"],
        "Tallier": []
    }

    # Call game_over
    result = game.game_over()
    print(f"Game over? {result}")

    # THIRD TEST

    print("THIRD TEST")


    # Create a test game instance
    game = WerewolfGame(w_aggro_vill_throw_fourp, "w_aggro_vill_throw_fourp")

    # Manually configure players for testing:
    # Example: all werewolves except Tallier (to trigger game over)
    game.current_players = {
        "Tallier": []
    }

    # Call game_over
    result = game.game_over()
    print(f"Game over? {result}")


    # FOURTH TEST

    print("FOURTH TEST")

    # Create a test game instance
    game = WerewolfGame(w_aggro_vill_throw_fourp, "w_aggro_vill_throw_fourp")

    # Manually configure players for testing:
    # Example: all werewolves except Tallier (to trigger game over)
    game.current_players = {
        "Player 1": ["werewolf", "TJ"],
        "Player 2": ["villager", "FP"],
        "Tallier": []
    }

    # Call game_over
    result = game.game_over()
    print(f"Game over? {result}")

    print("FIFTH TEST")

        # Create a test game instance
    game = WerewolfGame(w_aggro_vill_throw_fourp, "w_aggro_vill_throw_fourp")

    # Manually configure players for testing:
    # Example: all werewolves except Tallier (to trigger game over)
    game.current_players = {
        "Player 2": ["werewolf", "aggressive_werewolf"],
        "Tallier": []
    }

    # Call game_over
    result = game.game_over()
    print(f"Game over? {result}")


if __name__ == "__main__":
    test_check_game_over()
