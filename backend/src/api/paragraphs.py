
from fastapi import APIRouter
from utils.paragraphs import Paragraph
from fastapi.responses import JSONResponse
from fastapi import status


router = APIRouter()

@router.get('/loadparagraph')
async def loadparagraph(time: int = 30, difficulty: str = "Hard"):
    paragraph = Paragraph(time=time,difficulty=difficulty)
    p = await paragraph.get_paragraph()
    
    if p:
        return {
            "paragraphs":p
        }
    
    return JSONResponse(content="Error in loading paragraph please refresh the page!",status_code=status.HTTP_200_OK)


@router.post('/createparagraph', status_code=status.HTTP_201_CREATED)
async def create_paragraph(paragraph: str, time: int = 60, difficulty: str = "Medium"):
    p = Paragraph(time=time,difficulty=difficulty)
    id = await p.create_paragraph(paragraph=paragraph)

    
    return JSONResponse(content={
        "message": "paragraph created successfully",
        "id": id 
    }, status_code=status.HTTP_201_CREATED)

