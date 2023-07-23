from motor import motor_asyncio
import os 
import asyncio

# return a database object
# access any collection by client.collection_name
client = motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL'))
