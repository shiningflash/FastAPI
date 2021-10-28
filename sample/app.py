from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    active: Optional[bool] = True


@app.get('/')
def main():
    return {
        "message": "Hello World!"
    }


@app.get('/items/{id}')
def get_items(id: int, q: Optional[str] = None):
    return {
        "id": id
    }


@app.put('/items/{id}')
def update_item(id: int, item: Item):
    return {
        'id': id,
        'item name': item.name,
        'item price': item.price,
        'active': item.active
    }
