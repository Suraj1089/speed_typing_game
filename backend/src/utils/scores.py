# models.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class GameResult(BaseModel):
    username: str
    accuracy: float
    typing_speed: float