from pydantic import BaseModel, Field
from typing import List



class PlyerBase(BaseModel):
    pass 


class PlayerCreate(PlyerBase):
    username: str 
    accurency: int = Field(gt=0,lt=100)
    wpm: int = Field(gt=0)
    cpm: int = Field(gt=0)


class LobbyBase(BaseModel):
    _id: str 


class LobbyCreate(LobbyBase):
    name: str
    time: int
    difficulty: str = Field(default='Easy')
    players: List[PlayerCreate] = []



