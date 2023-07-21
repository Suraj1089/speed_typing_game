class Player:
    def __init__(self, player_id: str, player_name: str):
        self.player_id = player_id
        self.player_name = player_name
        self.speed = 0
        self.accuracy = 0

    def update_progress(self, user_input: str, challenge: str):
        accuracy = sum(a == b for a, b in zip(user_input, challenge)) / len(challenge) * 100
        speed = len(user_input.split()) / 1.0  # Words per minute

        self.speed = speed
        self.accuracy = accuracy

    def get_info(self):
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "speed": self.speed,
            "accuracy": self.accuracy
        }
