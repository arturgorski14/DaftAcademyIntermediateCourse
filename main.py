from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get('/counter')
def counter() -> str:
    app.counter += 1
    return str(app.counter)


@app.get("/hello/{name}", response_model=HelloResp)
def hello_name_view(name: str) -> HelloResp:
    return HelloResp(msg=f"Hello {name}")
