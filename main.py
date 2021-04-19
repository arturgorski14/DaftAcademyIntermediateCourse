import hashlib
import datetime

from typing import Optional
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel


class AppClass:
    APP_URL = "https://daft-academy-intermediate-2021.herokuapp.com"


app = FastAPI()
patients = {}


def next_patient_id(start):
    num = start
    while True:
        yield num
        num += 1


gen_patient_id = next_patient_id(start=1)


class Patient(BaseModel):
    id: Optional[int] = 0
    name: str
    surname: str
    register_date: Optional[str] = datetime.date.today().strftime("%Y-%m-%d")
    vaccination_date: Optional[str] = datetime.date.today().strftime("%Y-%m-%d")


@app.get("/")
async def root() -> dict:
    """Return dict with HelloWorld message."""
    return {"message": "Hello World"}


@app.get('/method')
async def get_method(request: Request):
    """Return dict with its request method name."""
    return {'method': request.method}


@app.post('/method', status_code=status.HTTP_201_CREATED)
async def get_method(request: Request):
    """Return dict with its request method name."""
    return {'method': request.method}


@app.delete('/method')
async def get_method(request: Request):
    return {'method': request.method}


@app.put('/method')
async def get_method(request: Request):
    return {'method': request.method}


@app.options('/method')
async def get_method(request: Request):
    return {'method': request.method}


@app.get('/auth')
async def auth(password: str, password_hash: str, response: Response):
    """Check if provided password and password_hash match."""
    h = hashlib.sha512(password.encode('utf-8'))

    if h.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(patient: Patient):

    today_date = datetime.date.today()
    vaccination_date = today_date + datetime.timedelta(len(patient.name) + len(patient.surname))

    new_id = next(gen_patient_id)
    patients[new_id] = Patient(
        id=new_id,
        name=patient.name,
        surname=patient.surname,
        register_date=today_date.strftime("%Y-%m-%d"),
        vaccination_date=vaccination_date.strftime("%Y-%m-%d")
    )

    return patients[new_id]


@app.get('/patient/{pid}')
async def get_patient(pid: int, response: Response):

    if pid < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST

    elif pid in patients:
        return patients[pid]

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
