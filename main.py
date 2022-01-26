from fastapi import FastAPI, Query, Body
from typing import Optional

from pydantic import BaseModel, HttpUrl, EmailStr


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


class Offer(BaseModel):
    name: str
    description: str
    price: int
    items: list[Item]


# UserIn 모델은 response body로 들어오며 새로운 유저를 만들기 위한 폼이다.
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# UserOut 모델은 생성된 유저에 대한 정보를 다시 클라이언트에게 보내게 되는 모델이다.
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


app = FastAPI()


# UserIn 모델을 생성하면, UserOut 모델의 필드만 값이 전달. (패스워드는 비밀 보장)
@app.post('/user', response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.get('/items', response_model=Item)
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})
    return item


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item_id(item_id: str):
    return items[item_id]


@app.post('/offer')
async def create_offer(offer: Offer):
    return offer


@app.post('/images/multiple/')
async def create_multiple_images(images: list[Image]):
    return images
