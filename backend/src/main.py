# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api import paragraphs,multiplayer,renders
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi import WebSocket,WebSocketDisconnect
from typing import List
import json
import requests

import os
app = FastAPI()

app.include_router(paragraphs.router)
app.include_router(multiplayer.router)
app.include_router(renders.router)
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



@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(os.getenv('MONGODB_URL'))
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
            print('message ', message)
 

manager = ConnectionManager()

@app.websocket("/ws/{username}/{lobby_id}")
async def websocket_endpoint(websocket: WebSocket, username: str, lobby_id: str):
    await manager.connect(websocket)
    print('helo')
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Erro in websocket")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    