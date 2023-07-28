from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Set

class Profile(BaseModel):
    name: str
    email: str
    age: int

class Product(BaseModel):
    name: str
    price: int = Field(
        title="Price of the item",
        description="This would be the price of the item.")
    discount: int
    discounted_price: float
    tags: Set[str] = []

class User(BaseModel):
    name: str
    email: str

app = FastAPI()

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