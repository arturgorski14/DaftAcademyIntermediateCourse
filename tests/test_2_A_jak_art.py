import pytest
from main import get_names_surname


@pytest.mark.parametrize('names_surname', [
    'hello', 'janko janeczko', 'ed edd eddy', '1234', 'anna kowalska', 'janek kos', 'jan sebastian bach'
])
def test_greetings(names_surname: str):
    assert f'Hello {names_surname.title()}' == get_names_surname(names_surname)
