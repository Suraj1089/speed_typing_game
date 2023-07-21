
from .database import db    
import uuid

class Paragraph:
    """
    Paragraph class to represent a paragraph for typing practice
    """
    def __init__(self, time: int, difficulty: str):
        self.time = time
        self.difficulty = difficulty

    def to_json(self,paragraph: str):
        return {
            "_id": str(uuid.uuid4()),  # Changed "id" to "_id" to match MongoDB primary key naming convention
            "time": self.time,
            "difficulty": self.difficulty,
            "paragraph": self.paragraph
        }
    
    async def create_paragraph(self,paragraph: str):
        print('create paragraph called')
        return await db["paragraphs"].insert_one(self.to_json(paragraph))  # Use await here to properly run the asynchronous method

    async def get_paragraph(self):
        paragraph = await db['paragraphs'].find_one({"time": self.time, "difficulty": self.difficulty})
        print(paragraph)
        if paragraph:
            return paragraph
        else:
            return None

    async def get_paragraph_by_id(self, id: str):
        paragraph = await db['paragraphs'].find_one({"_id": id})
        if paragraph:
            return paragraph
        else:
            return None

    def __repr__(self):
        return f"<Paragraph time={self.time} difficulty={self.difficulty} paragraph={self.paragraph}>"

