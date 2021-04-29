import datetime
import hashlib
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.templating import Jinja2Templates
from models.Patient import Patient
from typing import Dict


app = FastAPI()
templates = Jinja2Templates(directory='templates')

# ----------------------------- 1_D_jak_deploy -----------------------------
app.counter: int = 1
app.storage: Dict[int, Patient] = {}


@app.get("/")
async def root() -> Dict:
    """Return dict with HelloWorld message."""
    return {"message": "Hello world!"}


@app.api_route(
    path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], status_code=200
)
async def read_request(request: Request, response: Response) -> Dict:
    """Return dict with key 'method' and value its HTTP name."""
    request_method = request.method

    if request_method == "POST":
        response.status_code = status.HTTP_201_CREATED

    return {"method": request_method}


@app.get('/auth')
async def auth(password: str = '', password_hash: str = '') -> Response:
    """Check whether provided password and password_hash match; if so returns 204, otherwise 401."""
    authorized = False
    if password and password_hash:
        phash = hashlib.sha512(bytes(password, "utf-8")).hexdigest()
        authorized = phash == password_hash

    if authorized:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post('/register', status_code=201)  # technically a POST but it also returns an item
async def create_patient(patient: Patient) -> Patient:
    """Insert patient into dictionary; generate id and dates; returns saved object."""
    patient.id = app.counter
    app.storage[app.counter] = patient
    app.counter += 1
    return patient


@app.get("/patient/{patient_id}")
async def show_patient(patient_id: int) -> Patient:
    """Get patient with passed id"""
    if patient_id < 1:
        raise HTTPException(status_code=400, detail="Invalid patient id")

    if patient_id not in app.storage:
        raise HTTPException(status_code=404, detail="Patient not found")

    return app.storage[patient_id]

# ----------------------------- 3_F_jak_Fast -----------------------------
@app.get('/hello')
async def hello_today_date(response: Response, request: Request):
    response.headers["Content-Type"] = 'text/html; charset=UTF-8'
    return templates.TemplateResponse('hello_today_date.html', {
        'request': request,
        'response': response,
        'today_date': datetime.date.today()
    })
