import datetime
import hashlib
from fastapi import FastAPI, Request, Response, status
from utils import letter_count_in_word, next_patient_id
from models.Patient import Patient, PatientAPI

app = FastAPI()
patients = {}  # list would be good too
gen_patient_id = next_patient_id(start=1)


@app.get("/")
async def root() -> dict:
    """Return dict with HelloWorld message."""
    return {"message": "Hello world!"}


@app.get('/method')
@app.post('/method', status_code=status.HTTP_201_CREATED)
@app.delete('/method')
@app.put('/method')
@app.options('/method')
async def get_method(request: Request):
    """Return dict with its request method name."""
    return {'method': request.method}


@app.get('/auth', status_code=status.HTTP_401_UNAUTHORIZED)
async def auth(response: Response, password: str = '', password_hash: str = ''):
    """Check whether provided password and password_hash match."""
    if password != '' and password_hash != '':
        h = hashlib.sha512(password.encode('utf-8'))
        if h.hexdigest() == password_hash:
            response.status_code = status.HTTP_204_NO_CONTENT


@app.post('/register')
async def register(patient: PatientAPI, response: Response):
    """Insert patient into dictionary; generate id and dates; returns saved object."""

    today_date = datetime.date.today()
    vaccination_date = today_date + datetime.timedelta(
        letter_count_in_word(patient.name) + letter_count_in_word(patient.surname))

    new_id = next(gen_patient_id)
    patients[new_id] = Patient(
        id=new_id,
        name=patient.name,
        surname=patient.surname,
        register_date=today_date.strftime("%Y-%m-%d"),
        vaccination_date=vaccination_date.strftime("%Y-%m-%d")
    )

    response.status_code = status.HTTP_201_CREATED
    return patients[new_id]


@app.get('/patient/{pid}')
async def get_patient(pid: int, response: Response):
    """Get patient with passed id"""
    if pid < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
    elif pid in patients:
        response.status_code = status.HTTP_200_OK
        return patients[pid]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
