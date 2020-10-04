from fastapi import FastAPI
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
import aiomcache
import databases
import sqlalchemy

mysql = databases.Database("mysql://root:my-secret-pw@127.0.0.1:3306")

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine("mysql+mysqldb://root:my-secret-pw@127.0.0.1:3306")
metadata.create_all(engine)

class MongoResponse(Response):
    def __init__(self, content, *args, **kwargs):
        super().__init__(
            content=dumps(content),
            media_type="application/json",
            *args,
            **kwargs,
        )

mongo = AsyncIOMotorClient('mongodb://mongoadmin:secret@localhost:27017/?authSource=admin')
memcache = aiomcache.Client("127.0.0.1", 11211)

app = FastAPI()

docDB = mongo.sampleDB

@app.on_event("startup")
async def startup():
    await mysql.connect()

@app.on_event("shutdown")
async def shutdown():
    memcache.close()
    mongo.close()
    await mysql.disconnect()

@app.get("/ping")
def health_check():
    return {"status": "alive"}

@app.get("/mongo")
async def get_document():
    cached = await memcache.get(b"mongo")
    if not cached:
        result = await docDB.posts.find_one()
        result = dumps(result)
        await memcache.set(b"mongo", result.encode('UTF-8'))
        cached = result
    else:
        cached = cached.decode('UTF-8')
    return Response(content=cached, media_type="application/json")

@app.post("/mongo")
async def add_document(body: dict):
    result = await docDB.posts.insert_one(body)
    return {"msg": "ok"}

@app.get("/mysql")
async def get_record():
    return {"msg": "ok"}

@app.post("/mysql")
async def add_record():
    return {"msg": "ok"}

