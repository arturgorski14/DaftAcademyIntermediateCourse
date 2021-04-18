from fastapi.testclient import TestClient
import pytest
from main import app
import datetime

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}


@pytest.mark.parametrize('endpoint', ['/method'])
def test_method(endpoint: str):
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == {'method': "GET"}  # 'method' is left for clarity

    response = client.post(endpoint)
    assert response.status_code == 201
    assert response.json() == {'method': "POST"}

    response = client.delete(endpoint)
    assert response.status_code == 200
    assert response.json() == {'method': "DELETE"}

    response = client.put(endpoint)
    assert response.status_code == 200
    assert response.json() == {'method': "PUT"}

    response = client.options(endpoint)
    assert response.status_code == 200
    assert response.json() == {'method': "OPTIONS"}


@pytest.mark.parametrize('password,password_hash,expected_status_code', [
    ('test', 'test_hash', 401),
    ('abc', 'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f', 204),
    ('haslo', '013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215', 204),
    ('haslo', 'f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091', 401)
])
def test_auth(password: str, password_hash: str, expected_status_code: int):
    response = client.get(f'/auth?password={password}&password_hash={password_hash}')
    assert response.status_code == expected_status_code


@pytest.mark.parametrize('name,surname', [('Jan', 'Nowak')])
def test_register(name: str, surname: str):
    response = client.post('/register', {"name": "Jan", "surname": "Nowak"})
    assert response.status_code == 201
