import datetime
from hashlib import sha256, sha512
from fastapi import Cookie, Depends, FastAPI, Request, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from models.Patient import Patient
from typing import Dict, Optional
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory='templates')

# ----------------------------- session variables -----------------------------
app.counter: int = 1
app.storage: Dict[int, Patient] = {}
app.token: str = 'B9BB2B844D23372A5CEF5F5C1DEC7'

# ----------------------------- 1_D_jak_deploy -----------------------------
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
        phash = sha512(bytes(password, "utf-8")).hexdigest()
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


def check_credentials_and_return_status_code(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, '4dm1n')
    correct_password = secrets.compare_digest(credentials.password, 'NotSoSecurePa$$')
    if not (correct_username and correct_password):
        return status.HTTP_401_UNAUTHORIZED
    return status.HTTP_201_CREATED


@app.post('/login_session/')
async def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    response.status_code = check_credentials_and_return_status_code(credentials)
    response.set_cookie('session_token', app.token)


@app.post('/login_token')
async def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    response.status_code = check_credentials_and_return_status_code(credentials)
    response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    json_compatible_item_data = jsonable_encoder({'token': app.token})
    return JSONResponse(content=json_compatible_item_data, status_code=response.status_code)


def set_response_based_on_format(format: str) -> Response:
    sc = status.HTTP_200_OK
    responses = {'json': JSONResponse({"message": "Welcome!"}, status_code=sc),
                 'html': HTMLResponse('<h1>Welcome!</h1>', status_code=sc)}
    return responses[format] if format in responses else PlainTextResponse('Welcome!', status_code=sc)


@app.get('/welcome_session')
async def welcome_session(request: Request, format: str = ''):
    try:
        _ = request.cookies.pop('session_token')
        return set_response_based_on_format(format)
    except KeyError:
        return Response(content=None, status_code=status.HTTP_401_UNAUTHORIZED)


@app.get('/welcome_token')
async def welcome_token(token: str = '', format: str = ''):
    if 'token' in token:
        return set_response_based_on_format(format)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)
