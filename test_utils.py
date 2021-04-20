import pytest
from utils import letter_count_in_word, next_patient_id


@pytest.mark.parametrize('word,w_count', [
    ('Jan', 3),
    ('Kowalski', 8),
    ('Gr234zegorz', 8),
    ('1234', 0),
    ('ąćęłńóśźż', 9),
    ('ĄĆĘŁŃÓŚŹŻ', 9),
    ('!@#$%^&*()1234567890', 0)
])
def test_letter_count_in_word(word: str, w_count: int):
    assert letter_count_in_word(word) == w_count


@pytest.mark.parametrize('start', [1, 100])
def test_next_patient_id(start: id):
    generator = next_patient_id(start)
    for i in range(3):  # just test a few examples
        assert next(generator) == start + i
