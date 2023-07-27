from fastapi import FastAPI

app = FastAPI()

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
