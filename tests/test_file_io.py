import csv
import json
from pathlib import Path
from unittest.mock import patch
import pytest
from utils import file_io


@pytest.fixture
def sample_json_data():
    return {"electronics": [{"article": "123", "name": "Phone"}]}


@pytest.fixture
def sample_csv_data():
    return [
        {"article": "123", "name": "Phone", "description": "Smart\nphone", "application": "Use\ncarefully"},
        {"article": "456", "name": "Laptop", "description": "Gaming\nlaptop", "application": None},
    ]


def test_save_json_real_fs(sample_json_data, tmp_path: Path):
    with patch.object(file_io, "_root_dir", return_value=tmp_path):
        file_io.save_json(sample_json_data)

    expected_dir = tmp_path / "data" / "json"

    files = list(expected_dir.glob("*_products.json"))
    assert len(files) == 1
    saved = json.loads(files[0].read_text(encoding="utf-8"))
    assert saved == sample_json_data


def test_save_csv_real_fs(sample_csv_data, tmp_path: Path):
    with patch.object(file_io, "_root_dir", return_value=tmp_path):
        file_io.save_csv(sample_csv_data, "test")

    expected_dir = tmp_path / "data" / "csv"

    files = list(expected_dir.glob("*_test.csv"))
    assert len(files) == 1

    text = files[0].read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(text.splitlines(), delimiter=";"))
    assert len(rows) == 2
    assert rows[0]["description"] == "Smart phone"
    assert rows[1]["application"] == ""
