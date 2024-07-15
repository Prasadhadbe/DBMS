from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import MongoDB
import uvicorn

app = FastAPI()
db = MongoDB("mongodb://localhost:27017/", "yourDatabaseName", "yourCollectionName")

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/", response_model=str)
def create_item(item: Item):
    item_id = db.create_document(item.dict())
    return item_id

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str):
    item = db.read_document(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=int)
def update_item(item_id: str, item: Item):
    updated_count = db.update_document(item_id, item.dict())
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_count

@app.delete("/items/{item_id}", response_model=int)
def delete_item(item_id: str):
    deleted_count = db.delete_document(item_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_count

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
