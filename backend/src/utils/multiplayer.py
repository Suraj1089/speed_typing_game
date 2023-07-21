from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import random
import string

app = FastAPI()

lobbies = {}


def generate_random_challenge(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))


@app.post("/lobby", response_model=dict)
def create_lobby(difficulty: str):
    difficulty = difficulty.lower()
    if difficulty not in {"easy", "medium", "hard"}:
        raise HTTPException(status_code=400, detail="Invalid difficulty level")

    lobby_id = len(lobbies) + 1
    challenge_length = 50 + (25 * {"easy": 0, "medium": 1, "hard": 2}[difficulty])
    challenge = generate_random_challenge(challenge_length)

    lobbies[lobby_id] = {"difficulty": difficulty, "challenge": challenge, "players": {}}
    return {"lobby_id": lobby_id, "typing_challenge": challenge}


@app.post("/results", response_model=dict)
def save_results(lobby_id: int, user_input: str):
    if lobby_id not in lobbies:
        raise HTTPException(status_code=404, detail="Lobby not found")

    lobby = lobbies[lobby_id]
    challenge = lobby["challenge"]
    players = lobby["players"]

    accuracy = sum(a == b for a, b in zip(user_input, challenge)) / len(challenge) * 100
    speed = len(user_input.split()) / 1.0  # Words per minute

    player_name = f"Player{len(players) + 1}"
    players[player_name] = {"speed": speed, "accuracy": accuracy}

    results = [{"name": name, "speed": data["speed"], "accuracy": data["accuracy"]} for name, data in players.items()]
    return {"results": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
