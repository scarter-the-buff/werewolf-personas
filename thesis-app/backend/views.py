from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .game_logic.GameManager import GameManager

# Instantiate the GameManager
game_manager = GameManager()


@csrf_exempt
def button_click(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title", "Unknown")
            print("Django button click method activated!")
            print(title)  # Prints the button title to the console
            return JsonResponse({"message": f"Received: {title}"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def start_game_req(request):
    print("New game made!")
    game_manager.makeGame()