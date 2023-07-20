# main.py
from fastapi import FastAPI
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

app = FastAPI()

# Connect to MongoDB asynchronously
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["speed_typing_db"]
game_results_collection = db["game_results"]


# models.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class GameResult(BaseModel):
    username: str
    accuracy: float
    typing_speed: float


# main.py
from fastapi import HTTPException

@app.post("/register/")
async def register_user(user: User):
    # Implement user registration logic here asynchronously
    # Save the user data to the database asynchronously
    await db.user_collection.insert_one(user.dict())
    return {"message": "User registered successfully"}

@app.post("/save_game_result/")
async def save_game_result(game_result: GameResult):
    # Implement saving game result logic here asynchronously
    # Save the game result data to the database asynchronously
    await db.game_results_collection.insert_one(game_result.dict())
    return {"message": "Game result saved successfully"}

@app.get("/game_results/{username}/")
async def get_game_results(username: str):
    # Implement logic to retrieve game results for a specific username asynchronously
    # Retrieve game results from the database for the given username asynchronously
    cursor = db.game_results_collection.find({"username": username})
    results = []
    async for result in cursor:
        results.append(result)
    return {"results": results}


# Create Jinja2Templates instance for rendering templates
templates = Jinja2Templates(directory="templates")

# Mount the "static" directory to serve static files like CSS and JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# ... (Rest of the code)

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/game", response_class=HTMLResponse)
async def read_game(request: Request):
    # Generate a random text snippet to type (you can modify this logic)
    text_to_type = "This is a sample text for the typing game."

    # Render the game.html template with the generated text
    return templates.TemplateResponse("game.html", {"request": request, "text_to_type": text_to_type})

@app.get("/results", response_class=HTMLResponse)
async def read_results(request: Request):
    # Retrieve game results from the database for a specific username (you can modify this logic)
    username = "testuser"
    cursor = db.game_results_collection.find({"username": username})
    results = await cursor.to_list(length=100)

    # Render the results.html template with the retrieved results
    return templates.TemplateResponse("results.html", {"request": request, "results": results})