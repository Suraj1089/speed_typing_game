import motor.motor_asyncio
import os
import uuid
import asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://suraj:suraj@cluster0.fswur.mongodb.net/?retryWrites=true&w=majority")
db = client.tallycode


