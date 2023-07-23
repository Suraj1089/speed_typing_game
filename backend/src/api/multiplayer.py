
from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi import status
from utils.schemas.multiplayer import LobbyBase
from fastapi.encoders import jsonable_encoder
import uuid
from bson import ObjectId
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from datetime import timedelta,datetime


router = APIRouter()

# ge
@router.get('/getlobbies', status_code=status.HTTP_200_OK)
def get_lobbies(request: Request,limit: int = 10):
    lobbies = request.app.database['lobbies'].find({})
    lobbies_list = list(lobbies)
    for lobby in lobbies_list:
        lobby["_id"] = str(lobby["_id"])
    return {
        "lobbies": lobbies_list
    }

@router.get('/getlobby', status_code=status.HTTP_200_OK)
def get_lobby(request: Request,lobby_id: str = "lobby"):
    print(lobby_id)
    lobby = request.app.database['lobbies'].find_one({"_id": ObjectId(lobby_id)})
    lobby["_id"] = str(lobby["_id"])
    print(lobby)
    return lobby

@router.post('/createlobby', status_code=status.HTTP_201_CREATED)
async def create_lobby(request: Request, time: int = 60, difficulty: str = "Medium",players: int = 0,lobby_name: str = "Lobby"):
    lobby = LobbyBase(_id=lobby_name,time=time, difficulty=difficulty,players=players,name=lobby_name)
    print(lobby)
    new_lobby = request.app.database['lobbies'].insert_one(jsonable_encoder(lobby))
    return JSONResponse(content={
        "message": "lobby created successfully",
        "id": str(new_lobby.inserted_id)
    }, status_code=status.HTTP_201_CREATED)


@router.post('/createplayer', status_code=status.HTTP_201_CREATED)
async def create_player(request: Request,lobby_id: str = "lobby", username: str = "Player",wpm: int = 0,accuracy: int = 0):
    player = {
        "_id": str(uuid.uuid4()),
        "lobby_id": lobby_id,
        "name": username,
        "wpm": wpm,
        "accuracy": accuracy
    }
    new_player = request.app.database['players'].insert_one(player)
    return JSONResponse(content={
        "message": "player created successfully",
        "id": str(new_player.inserted_id)
    }, status_code=status.HTTP_201_CREATED)



@router.get('/getplayers', status_code=status.HTTP_200_OK)
def get_players(request: Request,lobby_id: str = "lobby"):
    players = request.app.database['players'].find({"lobby_id": lobby_id})
    players_list = list(players)
    for player in players_list:
        player["_id"] = str(player["_id"])
    return {
        "players": players_list
    }


@router.get('/gamestatus', status_code=status.HTTP_200_OK)
def game_status(request: Request, lobby_id: str,time: int,timer: int):
    lobby = request.app.database['lobbies'].find_one({"_id": ObjectId(lobby_id)})
    
    if lobby:
        if "start_time" not in lobby or "end_time" not in lobby:
            start_time = datetime.datetime.now()  
            end_time = start_time + datetime.timedelta(seconds=time) 
            
            request.app.database['lobbies'].update_one(
                {"_id": ObjectId(lobby_id)},
                {"$set": {"start_time": start_time, "end_time": end_time}}
            )
            lobby = request.app.database['lobbies'].find_one({"_id": ObjectId(lobby_id)})
            return JSONResponse(content=lobby, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=lobby, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Lobby not found"}, status_code=status.HTTP_404_NOT_FOUND)
