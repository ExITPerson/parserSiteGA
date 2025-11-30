import pytest

from utils.cleaner import clean_cell


@pytest.fixture
def text():
    return (f'Привет\n'
            f'рабочие\n'
            f'пролетариата')

def test_clean_cell(text):
    assert clean_cell(text) == 'Привет рабочие пролетариата'

def test_clean_cell_no_indents():
    text = 'Привет рабочие пролетариата от товарища Ленина'

    assert clean_cell(text) == 'Привет рабочие пролетариата от товарища Ленина'

def test_clean_cell_no_text():
    text = None
    assert clean_cell(text) == ''