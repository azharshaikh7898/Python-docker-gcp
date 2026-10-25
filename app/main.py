from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Cloud Run Demo API", version="1.0.0")

ITEMS: dict[int, dict] = {}


class Item(BaseModel):
    name: str
    price: float


@app.get("/")
def root():
    return {"message": "Hello from Cloud Run"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items/{item_id}", status_code=201)
def create_item(item_id: int, item: Item):
    if item_id in ITEMS:
        raise HTTPException(status_code=409, detail="Item already exists")
    ITEMS[item_id] = item.model_dump()
    return ITEMS[item_id]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return ITEMS[item_id]
