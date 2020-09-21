from fastapi import FastAPI
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
import aiomcache


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
mc = aiomcache.Client("127.0.0.1", 11211)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    mc.close()


@app.get("/ping")
def health_check():
    return {"status": "alive"}

@app.get("/mongo")
async def get_item():
    cached = await mc.get(b"mongo")
    if not cached:
        result = await db.posts.find_one()
        result = dumps(result)
        await mc.set(b"mongo", result.encode('UTF-8'))
        cached = result
    else:
        cached = cached.decode('UTF-8')
    return Response(content=cached, media_type="application/json")

@app.post("/mongo")
async def add_item(body: dict):
    result = await db.posts.insert_one(body)
    return {"msg": "ok"}
