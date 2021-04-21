import pytest
from main import get_names_surname


@pytest.mark.parametrize('names_surname', [
    'hello', 'janko janeczko', 'ed edd eddy', '1234'
])
def test_greetings(names_surname: str):
    ab = f'Hello {names_surname.title()}'
    print(ab)
    cd = get_names_surname(names_surname)
    print(cd)
    assert ab == cd
