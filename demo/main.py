from typing import Optional, List
from fastapi import FastAPI, Query, Path, Body, status, HTTPException
from pydantic import BaseModel, HttpUrl
from datetime import datetime, time, date, timedelta
from uuid import UUID

app = FastAPI(
    title = 'ITEM MANAGER',
    description = 'ITEM manager and tracker app'
)

class User(BaseModel):
    username: str
    full_name: str

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    user: Optional[User] = None
    images: Optional[List[Image]] = None

@app.get('/')
async def home():
    return {"Hello" : "world!"}

@app.put('/items/{item_id}')
async def update_items(item_id: int, item: Item):
    item.item_id = item_id
    return item

@app.post('/item/create/{item_id}', status_code=status.HTTP_201_CREATED)
async def create_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        **item.dict()
    }

@app.get('/items/{item_id}')
async def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-negative item id is not allowed."
        )
    return item_id

@app.put('/items/purchase/{item_id}')
async def update_purchase_item(item_id: int, item: Item):
    result = {
        'item_id': item_id,
        'item': item
    }
    return result

@app.put('/data/{item_id}')
async def get_data(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    process_after: Optional[timedelta] = Body(None),
    start_date: Optional[date] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_date": start_date,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration
    }
