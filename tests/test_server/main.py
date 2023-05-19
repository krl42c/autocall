from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name : str
    description : str
    price : float

@app.get("/")
async def root():
    return { "message" : "Hello world"}

@app.post("/item")
async def create_item(item : Item):
    return item

@app.post("/token")
async def token(client_id : str = "", client_secret=""):
    return "asd82732863hjnhsud8s787012938Ckwjhdns/DSWWED"
