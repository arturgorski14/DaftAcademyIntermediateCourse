from fastapi.testclient import TestClient
import pytest
from main import app, letter_count_in_word
import datetime

client = TestClient(app)


class TestDJakDeploy:
    """Test class for first lecture exercises"""
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {'message': 'Hello world!'}

    @pytest.mark.parametrize('method,expected_status_code,method_type', [
        (client.get('/method'), 200, 'GET'),
        (client.post('/method'), 201, 'POST'),
        (client.delete('/method'), 200, 'DELETE'),
        (client.put('/method'), 200, 'PUT'),
        (client.options('/method'), 200, 'OPTIONS')
    ])
    def test_method(self, method, expected_status_code: int, method_type: str):
        response = method
        assert response.status_code == expected_status_code
        assert response.json() == {'method': method_type}

    @pytest.mark.parametrize('password,password_hash,expected_status_code', [
        ('', 'cokolwiek', 401),
        ('', '', 401),
        ('cokolwiek', '', 401),
        ('test', 'test_hash', 401),
        ('abc', 'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f', 204),
        ('haslo', '013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215', 204),
        ('haslo', 'f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091', 401)
    ])
    def test_auth(self, password: str, password_hash: str, expected_status_code: int):
        response = client.get(f'/auth?password={password}&password_hash={password_hash}')
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize('name,surname,expected_id', [
        ('Jan', 'Nowak', 1),
        ('ąćęł', 'ńóśźż', 2),
        ('Marian Mario', '', 3),
        ('', 'Kowalski Sochoń', 4),
        ('!@#$%^&*()1234567890', 'Kowalski', 5),
        ('Jan Sebastian', 'Bach', 6),
        ('Jan', '!@#$%^&*()1234567890', 7)
    ])
    def test_register(self, name: str, surname: str, expected_id: int):
        response = client.post('/register', json={"name": name, "surname": surname})
        assert response.status_code == 201

        register_date = datetime.date.today()
        vaccination_date = register_date + datetime.timedelta(
            letter_count_in_word(name) + letter_count_in_word(surname))
        assert response.json() == dict(
            id=expected_id,
            name=name,
            surname=surname,
            register_date=register_date.strftime("%Y-%m-%d"),
            vaccination_date=vaccination_date.strftime("%Y-%m-%d")
        )

    @pytest.mark.parametrize('pid,expected_status_code,name,surname', [
        (1, 200, 'Jan', 'Nowak'),
        (3, 200, 'Marian Mario', ''),
        (4, 200, '', 'Kowalski Sochoń'),
        (6, 200, 'Jan Sebastian', 'Bach'),
        (7, 200, 'Jan', '!@#$%^&*()1234567890'),
        (8, 404, '', ''),
        (10000000, 404, '', ''),
        (-1, 400, '', ''),
        (0, 400, '', ''),
    ])
    def test_get_patient(self, pid: int, expected_status_code: int, name: str, surname: str):
        response = client.get(f'/patient/{pid}')
        assert response.status_code == expected_status_code
        if response.status_code == 200:
            assert response.json()['name'] == name
            assert response.json()['surname'] == surname
