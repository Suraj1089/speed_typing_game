
import motor.motor_asyncio
import os 
import uuid


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://suraj:suraj@cluster0.fswur.mongodb.net/?retryWrites=true&w=majority")
db = client.tallycode


class Paragraph:
    """
    Paragraph class to represent a paragraph for typing practice
    """
    def __init__(self, time: int, difficulty: str, paragraph: str):
        self.time = time
        self.difficulty = difficulty
        self.paragraph = paragraph

    def to_json(self):
        return {
            "id": str(uuid.uuid4()),
            "time": self.time,
            "difficulty": self.difficulty,
            "paragraph": self.paragraph
        }
    
    def create_paragraph(self):
        print('create paragraph called')
        return db["paragraphs"].insert_one(self.to_json())
    
    @staticmethod
    async def get_paragraph(time: int, difficulty: str):
        paragraph = await db.paragraphs.find_one({"time": time, "difficulty": difficulty})
        if paragraph:
            return paragraph
        else:
            return None
        
    @staticmethod
    async def get_paragraph_by_id(id: str):
        paragraph = await db.paragraphs.find_one({"_id": id})
        if paragraph:
            return paragraph
        else:
            return None

    def __repr__(self):
        return f"<Paragraph time={self.time} difficulty={self.difficulty} paragraph={self.paragraph}>"
    


p = Paragraph(30, "Hard", " decide what is the value and what will be the. How well one improves with practice depends on several factors, such as the frequency it is engaged in, and the type of feedback that is available for improvement. If feedback is not appropriate (either from an instructor or from self-reference to an information source),")
p.create_paragraph()
# print(p.ge)
print(p.get_paragraph(60, "Easy"))