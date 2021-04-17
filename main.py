from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class AppClass:
    APP_URL="daft-academy-intermediate-2021.heroku.com"


class HelloResp(BaseModel):
    msg: str


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get('/counter')
async def counter() -> str:
    app.counter += 1
    return str(app.counter)


@app.get("/hello/{name}", response_model=HelloResp)
async def hello_name_view(name: str) -> HelloResp:
    return HelloResp(msg=f"Hello {name}")


@app.get('/method/')
async def get_method(request: Request):
    """Return dict with request method. Success status codes are handled by path decorators."""
    return {'method': request.method}


@app.post('/method/post/')
async def post_method(item: HelloResp, request: Request):
    return item


@app.delete('/method/delete/{item_id}')
async def delete_method(item_id: int, request: Request):
    return {'method': request.method}


@app.put('/method/update/{item_id}')
async def put_method(item_id: int, request: Request):
    return {'method': request.method}


@app.options('/method/options/')
async def options_method(request: Request):
    return {'method': request.method}


@app.get('/auth/{password}/{password_hash}')
def auth(password: str='', password_hash: str=''):
    return pass
