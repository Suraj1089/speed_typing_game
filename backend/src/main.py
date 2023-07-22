# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api import paragraphs,multiplayer
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi import WebSocket,WebSocketDisconnect
from typing import List
import json
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



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            print('message ',message)
 

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = f'{"username":{username}, "action": "left"}'
        await manager.broadcast(message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    