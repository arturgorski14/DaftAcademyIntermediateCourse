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

    response = client.post(f"/method/post")
    assert response.status_code == 307
    # assert response.json() == {'method': "POST"}

    response = client.delete(f"/method/delete/3")
    assert response.status_code == 200
    assert response.json() == {'method': "DELETE"}

    response = client.put(f"/method/update/3")
    assert response.status_code == 200
    assert response.json() == {'method': "PUT"}

    response = client.put(f"/method/options")
    assert response.status_code == 307
    # assert response.json() == {'options': "OPTIONS"}
