import asyncio
import motor.motor_asyncio
import uuid
import random
import string

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://suraj:suraj@cluster0.fswur.mongodb.net/?retryWrites=true&w=majority")
db = client.tallycode


class Lobby:
    def __init__(self, lobby_id: int, difficulty: str):
        self.lobby_id = lobby_id
        self.difficulty = difficulty

