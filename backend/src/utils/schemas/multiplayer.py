from pydantic import BaseModel
from typing import List



class PlyerBase(BaseModel):
    _id: str 


class PlayerCreate(PlyerBase):
    username: str 
    accurency: int = 0
    wpm: int = 0
    cpm: int = 0


class LobbyBase(BaseModel):
    _id: str 


class LobbyCreate(LobbyBase):
    name: str
    time: int
    difficulty: str 
    players: List[PlayerCreate] = []



