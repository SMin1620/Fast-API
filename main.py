from fastapi import FastAPI, Query, Body
from typing import Optional

from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = set()
    image: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str
    price: int
    items: list[Item]


app = FastAPI()


@app.get('/items')
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})
    return item


@app.put("/items/{item_id}")
async def upgrade_item(item_id: int, item: Item):
    results = {'item_id': item_id, 'item': item}
    return results


@app.post('/offer')
async def create_offer(offer: Offer):
    return offer


@app.post('/images/multiple/')
async def create_multiple_images(images: list[Image]):
    return images

