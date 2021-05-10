import datetime
import secrets
import sqlite3
from hashlib import sha256, sha512
from typing import Dict, Optional

from fastapi import (Cookie, Depends, FastAPI, HTTPException, Request,
                     Response, status)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils import tags_metadata

from models.Patient import Patient

# ----------------------------- startup -----------------------------

app = FastAPI(openapi_tags=tags_metadata.tags_metadata)
security = HTTPBasic()
templates = Jinja2Templates(directory='templates')
app.counter: int = 1
app.storage: Dict[int, Patient] = {}


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

# ----------------------------- 1_D_jak_deploy -----------------------------
@app.get("/", tags=['first_lecture'])
async def root() -> Dict:
    """Return dict with HelloWorld message."""
    return {"message": "Hello world!"}


@app.api_route(
    path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], status_code=200, tags=['first_lecture']
)
async def read_request(request: Request, response: Response) -> Dict:
    """Return dict with key 'method' and value its HTTP name."""
    request_method = request.method

    if request_method == "POST":
        response.status_code = status.HTTP_201_CREATED

    return {"method": request_method}


@app.get('/auth', tags=['first_lecture'])
async def auth(password: str = '', password_hash: str = '') -> Response:
    """Check whether provided password and password_hash match; if so returns 204, otherwise 401."""
    authorized = False
    if password and password_hash:
        phash = sha512(bytes(password, "utf-8")).hexdigest()
        authorized = phash == password_hash

    if authorized:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post('/register', status_code=201, tags=['first_lecture'])  # technically a POST but it also returns an item
async def create_patient(patient: Patient) -> Patient:
    """Insert patient into dictionary; generate id and dates; returns saved object."""
    patient.id = app.counter
    app.storage[app.counter] = patient
    app.counter += 1
    return patient


@app.get("/patient/{patient_id}", tags=['first_lecture'])
async def show_patient(patient_id: int) -> Patient:
    """Get patient with passed id"""
    if patient_id < 1:
        raise HTTPException(status_code=400, detail="Invalid patient id")

    if patient_id not in app.storage:
        raise HTTPException(status_code=404, detail="Patient not found")

    return app.storage[patient_id]

# ----------------------------- 3_F_jak_Fast -----------------------------
@app.get('/hello', tags=['third_lecture'])
async def hello_today_date(response: Response, request: Request):
    response.headers["Content-Type"] = 'text/html; charset=UTF-8'
    return templates.TemplateResponse('hello_today_date.html', {
        'request': request,
        'response': response,
        'today_date': datetime.date.today()
    })


def check_credentials_and_return_status_code(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, '4dm1n')
    correct_password = secrets.compare_digest(credentials.password, 'NotSoSecurePa$$')
    if not (correct_username and correct_password):
        return status.HTTP_401_UNAUTHORIZED
    return status.HTTP_201_CREATED


@app.post('/login_session/', tags=['third_lecture'])
async def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    response.status_code = check_credentials_and_return_status_code(credentials)
    response.set_cookie('session_token', 'apptoken')


@app.post('/login_token', tags=['third_lecture'])
async def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    response = JSONResponse()
    response.content = {'token': 'apptoken'}
    response.status_code = check_credentials_and_return_status_code(credentials)
    response.set_cookie('token', 'apptoken')


def set_response_based_on_format(format: str) -> Response:
    sc = status.HTTP_200_OK
    responses = {'json': JSONResponse({"message": "Welcome!"}, status_code=sc),
                 'html': HTMLResponse('<h1>Welcome!</h1>', status_code=sc)}
    return responses[format] if format in responses else PlainTextResponse('Welcome!', status_code=sc)


@app.get('/welcome_session', tags=['third_lecture'])
async def welcome_session(request: Request, format: str = ''):
    try:
        if not request.cookies.get('session_token'):
            raise KeyError
        return set_response_based_on_format(format)
    except KeyError:
        return PlainTextResponse('Welcome!', status_code=status.HTTP_401_UNAUTHORIZED)


@app.get('/welcome_token', tags=['third_lecture'])
async def welcome_token(request: Request, token: str = '', format: str = ''):
    try:
        if request.cookies.get('token') != token:
            raise KeyError
        return set_response_based_on_format(format)
    except KeyError:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

# ----------------------------- 4_T_jak_tabela -----------------------------
@app.get('/categories', tags=['fourth_lecture'])
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
        SELECT CategoryID, CategoryName
        FROM Categories
        ORDER BY CategoryID
    ''').fetchall()
    return {'categories': [{"id": x['CategoryID'], "name": x["CategoryName"]} for x in data]}


@app.get('/customers', tags=['fourth_lecture'])
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
        SELECT CustomerID, CompanyName, Address, PostalCode, City, Country
        FROM CUSTOMERS
        ORDER BY CustomerID
    ''').fetchall()
    return {'customers': [{
        "id": x['CustomerID'],
        "name": x["CompanyName"],
        "full_address": f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"
    } for x in data]}
