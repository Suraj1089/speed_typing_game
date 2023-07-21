
from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from fastapi import status
from utils.schemas.paragraphs import ParagraphBase
from fastapi.encoders import jsonable_encoder
import uuid
from bson import ObjectId



router = APIRouter()

@router.get('/loadparagraph',status_code=status.HTTP_200_OK)
async def load_paragraph(request: Request, time: int, difficulty: str):
    # Query the MongoDB collection for paragraphs with matching time and difficulty
    paragraphs = request.app.database["paragraphs"].find({"time": time, "difficulty": difficulty}).limit(10)
    paragraphs_list = list(paragraphs)
    # Convert the ObjectId to a string in each paragraph dictionary
    for paragraph in paragraphs_list:
        paragraph["_id"] = str(paragraph["_id"])
    
    if len(paragraphs_list) == 0:
        return JSONResponse(
            content="Error in loading paragraph try again",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return {
        "paragraph":paragraphs_list
    }
    


@router.post('/createparagraph', status_code=status.HTTP_201_CREATED)
async def create_paragraph(request: Request, time: int = 60, difficulty: str = "Medium"):
    data = await request.json()
    paragraph = data['paragraph']
    p = ParagraphBase(_id=str(ObjectId()), time=time, difficulty=difficulty, paragraph=paragraph)
    new_paragraph = request.app.database['paragraphs'].insert_one(jsonable_encoder(p))
    return JSONResponse(content={
        "message": "paragraph created successfully",
        "id": str(new_paragraph.inserted_id)
    }, status_code=status.HTTP_201_CREATED)
