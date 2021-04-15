from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name: str):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json()['msg'] == f"Hello {name}"


@pytest.mark.parametrize("counter", [2])
def test_counter(counter):
    for i in range(counter):
        response = client.get(f"/counter")
        assert response.status_code == 200
        assert response.json() == str(i+1)
