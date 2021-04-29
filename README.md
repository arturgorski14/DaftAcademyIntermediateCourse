# Daft Academy Intermediate Course

Web API created in FastAPI and deployed on Heroku for learning purposes.

## Documentation and endpoints
https://daft-academy-intermediate-2021.herokuapp.com/docs

## Used Technologies
* [FastAPI](https://fastapi.tiangolo.com/)
* Python 3.8.7
* [Pytest](https://docs.pytest.org/en/6.2.x/).

## Setup
To run this project enable virtual environment:
```
$ python3 -m venv venv-daft-intermediate-3.8.7
$ source venv-daft-intermediate-3.8.7/bin/activate
```
more methods https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b

Install required packages
```
$ pip3 install poetry
$ poetry install
```
or
```
$ pip3 install -r requirements.txt
```

Run server locally:
```
$ uvicorn main:app
```