import csv
import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.cleaner import clean_cell


logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(
        "logs/product_article.log",
        encoding="utf-8",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def _root_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def save_json(data: dict) -> None:
    """Сохраняет словарь в json файл"""
    if not data:
        logger.warning("save_json: пустой словарь, файл не создан")
        return

    filepath = _root_dir() / "data" / "json"
    filepath.mkdir(parents=True, exist_ok=True)

    filename = filepath / f"{datetime.now():%Y-%m-%d}_products.json"
    logger.debug("Сохраняем JSON в %s", filename)

    try:
        with filename.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info("JSON успешно сохранён: %s", filename.name)

    except Exception as e:
        logger.exception(f"Ошибка сохранения JSON файла: {e}")


def save_csv(data: list, file_name: str) -> None:
    if not data:
        logger.warning("save_csv: пустой список, файл не создан")
        return

    filepath = _root_dir() / "data" / "csv"
    filepath.mkdir(parents=True, exist_ok=True)

    now_str = datetime.now().strftime("%Y-%m-%d")
    filename = filepath / f"{now_str}_{file_name}.csv"
    logger.debug("Сохраняем CSV в %s", filename)

    fieldnames = data[0].keys()

    for item in data:
        item["description"] = clean_cell(item["description"])
        item["application"] = clean_cell(item["application"])

    try:
        with filename.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        logger.info("CSV успешно сохранён: %s", filename.name)

    except Exception as e:
        logger.exception(f"Ошибка сохранения CSV файла {e}")
