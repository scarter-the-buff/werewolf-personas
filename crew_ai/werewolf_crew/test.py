# test.py
from werewolfGame import WerewolfGame

w_aggro_vill_throw_fourp = {
    "Player 1": ["werewolf", "aggressive_werewolf"],
    "Player 2": ["werewolf", "aggressive_werewolf"],
    "Player 3": ["villager", "not_trying_villager"],
    "Player 4": ["villager", "not_trying_villager"],
    "Tallier": []
}


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
    test_game_over()
