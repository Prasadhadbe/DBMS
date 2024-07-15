from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List  
from database import MongoDB
from bson import ObjectId
import uvicorn

app = FastAPI()
db = MongoDB("mongodb://localhost:27017/", "yourDatabaseName", "yourCollectionName")

class Item(BaseModel):
    name: str
    description: str = None

def is_valid_object_id(id: str) -> bool:
    try:
        ObjectId(id)
        return True
    except Exception:
        return False

@app.post("/items/", response_model=str)
def create_item(item: Item):
    item_id = db.create_document(item.dict())
    return item_id

@app.get("/items/", response_model=List[Item])  # Updated endpoint for fetching all items
def read_all_items():
    items = db.collection.find()  # Fetch all documents from MongoDB collection
    return list(items)  # Convert pymongo Cursor to list of dictionaries

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str):
    if not is_valid_object_id(item_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    item = db.read_document(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=int)
def update_item(item_id: str, item: Item):
    if not is_valid_object_id(item_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    updated_count = db.update_document(item_id, item.dict())
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_count

@app.delete("/items/{item_id}", response_model=int)
def delete_item(item_id: str):
    if not is_valid_object_id(item_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    deleted_count = db.delete_document(item_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_count

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
