from pydantic import BaseModel


class LobbyBase(BaseModel):
    _id: str 
    time: int
    difficulty: str 
    players: int = 0
    name: str
