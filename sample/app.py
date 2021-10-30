from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class CategoryChoice(str, Enum):
    food = 'food'
    medicine = 'medicine'
    stationary = 'stationary'


class Item(BaseModel):
    name: str
    price: float
    vat: Optional[bool] = False
    category: CategoryChoice


@app.get('/')
async def main():
    return {
        "message": "Hello World!"
    }


@app.get('/items/{id}')
async def get_items(
        id: int,
        q: Optional[str] = None,
        category: CategoryChoice = Query(..., min_length=3, max_length=50, regex="^[0-9]*$")
    ):
    return {
        "id": id,
        "q": q,
        "category": category
    }


@app.put('/items/{id}')
async def update_item(id: int, item: Item):
    item_dict = item.dict()
    item_dict.update({
        "id": id
    })
    if item.vat:
        item_dict.update({
            "price_with_vat": item.price + (item.price * 25) / 100
        })
    return item_dict
