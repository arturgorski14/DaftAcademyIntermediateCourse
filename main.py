import hashlib

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class AppClass:
    APP_URL = "https://daft-academy-intermediate-2021.heroku.com"


@app.get("/")
async def root() -> dict:
    """Return dict with HelloWorld message."""
    return {"message": "Hello World"}


@app.get('/method/')
async def get_method(request: Request):
    """Return dict with its request method name."""
    return {'method': request.method}


@app.post('/method/', status_code=status.HTTP_201_CREATED)
async def get_method(request: Request):
    """Return dict with its request method name."""
    return {'method': request.method}


@app.delete('/method/')
async def get_method(request: Request):
    return {'method': request.method}


@app.put('/method/')
async def get_method(request: Request):
    return {'method': request.method}


@app.options('/method/')
async def get_method(request: Request):
    return {'method': request.method}


@app.get('/auth/')
def auth(password: str, password_hash: str, response: Response):
    """Check if provided password and password_hash match."""
    h = hashlib.sha512(password.encode('utf-8'))

    if h.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
