import pytest
from main import get_names_surname, sentence


@pytest.mark.parametrize('names_surname', [
    'hello', 'janko janeczko', 'ed edd eddy', '1234', 'anna kowalska', 'janek kos', 'jan sebastian bach'
])
def test_greetings(names_surname: str):
    assert f'Hello {names_surname.title()}' == get_names_surname(names_surname)


@pytest.mark.parametrize('text,is_pal', [
    ('annA', True),
    ('Łapał za kran, a kanarka złapał', True),
    ('Ka5j5aK', True),
    ('A_CCA$', True),
    ('Eva, can I see bees in a cave?', True),
    ('Sir, I demand, I am a maid named Iris.', True),
    ('123354aba3454235', False)
])
def test_is_palindrome(text: str, is_pal: int):
    is_or_not_palindrome = ' - is palindrome' if is_pal else ' - is not palindrome'
    assert f'{text}{is_or_not_palindrome}' == sentence(text)
