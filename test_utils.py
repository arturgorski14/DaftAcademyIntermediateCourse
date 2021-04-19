import pytest
from utils import letter_count_in_word


@pytest.mark.parametrize('word,w_count', [
    ('Jan', 3),
    ('Kowalski', 8),
    ('Gr234zegorz', 8),
    ('1234', 0),
    ('ąćęłńóśźż', 9),
    ('ĄĆĘŁŃÓŚŹŻ', 9)
])
def test_letter_count_in_word(word: str, w_count: int):
    assert letter_count_in_word(word) == w_count
