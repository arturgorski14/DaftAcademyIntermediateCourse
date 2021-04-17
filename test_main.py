from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_method():
    response = client.get(f"/method/")
    assert response.status_code == 200
    assert response.json() == {'method': "GET"}

    response = client.post(f"/method/")
    assert response.status_code == 201
    assert response.json() == {'method': "POST"}

    response = client.delete(f"/method/")
    assert response.status_code == 200
    assert response.json() == {'method': "DELETE"}

    response = client.put(f"/method/")
    assert response.status_code == 200
    assert response.json() == {'method': "PUT"}

    response = client.options(f"/method/")
    assert response.status_code == 200
    assert response.json() == {'method': "OPTIONS"}


def test_auth():
    response = client.get("/auth/")
    assert response.status_code == 401
