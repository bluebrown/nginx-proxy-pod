from fastapi import FastAPI
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps

class MongoResponse(Response):
    def __init__(self, content, *args, **kwargs):
        super().__init__(
            content=dumps(content),
            media_type="application/json",
            *args,
            **kwargs,
        )

client = AsyncIOMotorClient(
    'mongodb://mongoadmin:secret@localhost:27017/?authSource=admin'
)
db = client.sampleDB
app = FastAPI()

@app.get("/ping")
def health_check():
    return {"status": "alive"}

@app.get("/mongo")
async def get_item():
    result = await db.posts.find_one()
    return MongoResponse(result)

@app.post("/mongo")
async def add_item(body: dict):
    result = await db.posts.insert_one(body)
    return {"msg": "ok"}
