# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api import paragraphs,multiplayer
# from api.socket import sio_app
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi import WebSocket,WebSocketDisconnect
import socketio
from typing import List

app = FastAPI()


app.include_router(paragraphs.router)
app.include_router(multiplayer.router)
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Jinja2Templates instance for rendering templates
templates = Jinja2Templates(directory="../../frontend")

# Mount the "static" directory to serve static files like CSS and JavaScript
app.mount("/static", StaticFiles(directory="../../frontend/assets"), name="static")




@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/practice", response_class=HTMLResponse)
async def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("practice.html", {"request": request})

@app.get('/about',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {"request": request})

@app.get('/profile',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('profile.html', {"request": request})

@app.get('/testimonials',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('testimonials.html', {"request": request})

@app.get('/practice/typing',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('typing.html', {"request": request})


@app.get('/multiplayer', response_class=HTMLResponse)
def multiplayer_mode(request: Request):
    # lobbiaes = requests.get('http://localhost:8000/getlobbies').json()
    # print(lobbies)
    return templates.TemplateResponse('multiplayer.html',{"request": request})


@app.get('/multiplayer/typing', response_class=HTMLResponse)
def multiplayer_lobby(request: Request,time: int = 60, difficulty: str = "Easy",lobby_id: str = "Easy one",username: str = None):
    return templates.TemplateResponse('multiplayer_lobby.html',{"request": request, "lobby_id": lobby_id
    , "time": time, "difficulty": difficulty, "username": username})


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient('mongodb+srv://suraj:suraj@cluster0.fswur.mongodb.net/?retryWrites=true&w=majority')
    app.database = app.mongodb_client["tallycode"]


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()



class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.active_connections.remove((websocket, user))

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection[0].send_json(data)    

manager = SocketManager()

@app.websocket("/sio")
async def chat(websocket: WebSocket):
    print("***************************************************************** websocket")
    await websocket.accept()
    while True:
        print('true ^^^^^^^^^^^^^^^^^')
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    