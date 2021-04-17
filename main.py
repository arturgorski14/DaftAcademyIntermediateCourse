from fastapi import FastAPI, Request, status
from pydantic import BaseModel
from hashlib import sha512

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


@app.post('/method/', status_code=201)
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
def auth(password: str, password_hash: str, request: Request):
    """Check if provided password and password_hash match."""
    if sha512(password) == password_hash:
        return _, status.HTTP_204_NO_CONTENT
    else:
        return _, status.HTTP_401_UNAUTHORIZED
