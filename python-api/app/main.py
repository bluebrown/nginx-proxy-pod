from fastapi import FastAPI
import motor.motor_asyncio

from fastapi.responses import Response
from bson.json_util import dumps


class MongoResponse(Response):
    def __init__(self, content, *args, **kwargs):
        super().__init__(
            content=dumps(content),
            media_type="application/json",
            *args,
            **kwargs,
        )


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongoadmin:secret@localhost:27017/?authSource=admin')
db = client.sampleDB

app = FastAPI()


@app.get("/ping")
def root():
    return {"status": "alive"}


@app.get("/mongo")
async def mongo():
    result = await db.posts.find_one()
    return MongoResponse(result)

