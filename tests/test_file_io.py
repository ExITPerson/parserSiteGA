import io
import json
import csv
from unittest.mock import patch, MagicMock
import pytest
from utils import file_io


@pytest.fixture
def sample_data():
    return [
        {"article": "123", "name": "Тест", "description": "Описание\nс переносом"},
        {"article": "456", "name": "Test2", "description": "Simple"},
    ]

@pytest.fixture
def sample_data_for_csv():
    return [
        {"article": "123", "name": "Тест", "description": "Описание\nс переносом", "application": "Нанести\nна кожу"},
        {"article": "456", "name": "Test2", "description": "Simple", "application": None},
    ]

def test_save_json_unit(sample_data):
    """Юнит-тест: записываем в память, не трогая диск."""
    buffer = io.StringIO()

    fake_file = MagicMock()
    fake_file.__enter__.return_value = buffer
    fake_file.__exit__.return_value = None

    with patch("utils.file_io.open", create=True) as mock_open:
        mock_open.return_value = fake_file

        file_io.save_json(sample_data)

    assert buffer.getvalue() == json.dumps(
        sample_data,
        ensure_ascii=False,
        indent=4
    )

def test_save_csv_unit(sample_data_for_csv):
    buffer = io.StringIO()

    # заглушка для контекстного менеджера
    fake_file = MagicMock()
    fake_file.__enter__.return_value = buffer
    fake_file.__exit__.return_value = None

    with patch("utils.file_io.open", create=True, return_value=fake_file):
        # Мокаем datetime, чтобы имя файла было стабильным
        with patch("utils.file_io.datetime") as mock_dt:
            mock_dt.now.return_value.date.return_value = "2025-12-01"

            file_io.save_csv(sample_data_for_csv, "products")

    # --- проверяем содержимое «файла» ---
    buffer.seek(0)
    reader = csv.DictReader(buffer, delimiter=";")
    rows = list(reader)

    # Проверяем, что clean_cell отработал (в вашей функции)
    assert rows[0]["description"] == "Описание с переносом"
    assert rows[0]["application"] == "Нанести на кожу"
    assert rows[1]["description"] == "Simple"
    assert rows[1]["application"] == ""