from pydantic import BaseModel


class ParagraphBase(BaseModel):
    _id: str 
    time: int
    difficulty: str 
    paragraph: str 

