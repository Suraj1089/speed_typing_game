from ..database import client
from typing import List
from schemas.multiplayer import PlayerCreate


class Player:
    """
    Represents a player in the Tallycode application.

    ### Attributes:
        db (pymongo.database.Database): The MongoDB database 'tallycode'.
        players (pymongo.collection.Collection): The collection 'players' in the 'tallycode' database.

    ### Methods:
        get(username: str = None, limit: int = 10, order: List[str] = []) -> List[str]:
            Retrieves a list of players from the database.
            If `username` is provided, it returns players with the given username.
            The `limit` parameter specifies the maximum number of players to retrieve.

        create(username: str):
            Creates a new player with the provided `username`, setting accuracy, WPM, and CPM to 0.
    """
    def __init__(self) -> None:
        self.db = client['tallycode']
        self.players = self.db.players

    async def get(self, username: str = None, limit: int = 10, order: List[str] = []) -> List[str]:
        # get all players
        if username is None:
            players = self.players.find().sort(order).limit(limit)
            return players.to_list()
        # if username is present return players by username
        player = self.players.find(filter={'username': username})
        return players

    async def create(self,usernmae: str):
        player = PlayerCreate(username=usernmae,accurency=0,wpm=0,cpm=0)
        result = await self.players.insert_one(player)
        return result.inserted_id
    



         
p = Player()
