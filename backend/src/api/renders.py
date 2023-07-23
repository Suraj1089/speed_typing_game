# main.py
from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


router = APIRouter(
    tags=['Templates']
)


templates = Jinja2Templates(directory="../../frontend")

# Mount the "static" directory to serve static files like CSS and JavaScript
router.mount("/static", StaticFiles(directory="../../frontend/assets"), name="static")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/practice", response_class=HTMLResponse)
async def home(request: Request):
    # Render the home.html template
    return templates.TemplateResponse("practice.html", {"request": request})

@router.get('/about',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {"request": request})

@router.get('/profile',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('profile.html', {"request": request})

@router.get('/testimonials',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('testimonials.html', {"request": request})

@router.get('/practice/typing',response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('typing.html', {"request": request})


@router.get('/multiplayer', response_class=HTMLResponse)
def multiplayer_mode(request: Request):
    # lobbiaes = requests.get('http://localhost:8000/getlobbies').json()
    return templates.TemplateResponse('multiplayer.html',{"request": request})


@router.get('/multiplayer/typing', response_class=HTMLResponse)
def multiplayer_lobby(request: Request,time: int = 60, difficulty: str = "Easy",lobby_id: str = "Easy one",username: str = None):
    return templates.TemplateResponse('multiplayer_lobby.html',{"request": request, "lobby_id": lobby_id
    , "time": time, "difficulty": difficulty, "username": username})
