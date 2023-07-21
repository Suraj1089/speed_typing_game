# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi_socketio import SocketManager
from api import paragraphs
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
import uuid
import asyncio



app = FastAPI()
app.include_router(paragraphs.router)
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
    return templates.TemplateResponse('multiplayer.html',{"request": request})

@app.get('/multiplayer/typing', response_class=HTMLResponse)
def multiplayer_lobby(request: Request,lobby_id: str = "suraj"):
    print('lobby_id',lobby_id)
    return templates.TemplateResponse('multiplayer_lobby.html',{"request": request, "lobby_id": lobby_id})


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient('mongodb+srv://suraj:suraj@cluster0.fswur.mongodb.net/?retryWrites=true&w=majority')
    app.database = app.mongodb_client["tallycode"]


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    socket_manager = SocketManager(app=app)