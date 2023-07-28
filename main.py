from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List
from uuid import UUID
from datetime import date, datetime, time, timedelta

class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta

class Profile(BaseModel):
    name: str
    email: str
    age: int

class Image(BaseModel):
    url: HttpUrl
    name: str

class Product(BaseModel):
    name: str = Field(example="phone")
    price: int = Field(
        title="Price of the item",
        description="This would be the price of the item.")
    discount: int
    discounted_price: float
    tags: Set[str] = Field(example="[electronics, phones]")
    image: List[Image]

    class Config:
        schema_extra={
            "example": {
                "name":"Phone",
                "price":100,
                "discount":10,
                "discounted_price":0,
                "tags":["Electronics", "Computers"],
                "image":[
                    {
                        "url":"http://www.foo.com",
                        "name":"phone image"
                    },
                    {
                        "url":"http://www.foo.com",
                        "name":"phone image side view"
                    }
                ]
            }
        }



class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product]

class User(BaseModel):
    name: str
    email: str

app = FastAPI()

@app.post('/addevent')
def addevent(event: Event):
    return event

@app.post('/addoffer')
def addoffer(offer: Offer):
    return {offer}

@app.post('/purchase')
def purchase(user: User, product:Product):
    return {'user':user, 'product': product}

@app.post('/addproduct/{product_id}')
def addproduct(product:Product, product_id:int, category:str):
    product.discounted_price = product.price - (product.price * product.discount)/100
    return {"product_id": product_id, "product": product, "category": category}

# admin takes precedence over username
@app.get('/user/admin')
def admin():
    return {'this is the admin page'}

@app.get('/user/{username}')
def user(username):
    return {f'this is a profile page for {username}'}

# query parameter ?id=<somenumber>&price=<somenumber>
# None makes price optional
@app.get('/products')
def products(id:int = 1, price:int=None):
    return {f'Product with an id: {id} and price {price}'}

# path with path and query parameters
@app.get('/profile/{userid}/comments')
def profile(userid:int,commentid:int):
    return {f'Profile page for user with id {userid} and commentid {commentid}'}

@app.post('/adduser')
def adduser(profile:Profile):
    return profile