import csv
import json
from datetime import datetime
from pathlib import Path

from utils.cleaner import clean_cell


ROOT_DIR = Path(__file__).resolve().parent.parent

def save_json(data):

    filepath = ROOT_DIR / 'data' / 'json'
    filepath.parent.mkdir(parents=True, exist_ok=True)

    now_date = datetime.now().date()

    try:
        with open(f'{filepath}/{now_date}_products.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f'Ошибка сохранения json файла: {e}')

def save_csv(data, file_name):

    filepath = ROOT_DIR / 'data' / 'csv'
    filepath.parent.mkdir(parents=True, exist_ok=True)

    now_date = datetime.now().date()

    fieldnames = data[0].keys()

    for item in data:
        item['description'] = clean_cell(item['description'])
        item['application'] = clean_cell(item['application'])

    try:
        with open(f'{filepath}/{now_date}_{file_name}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)

    except Exception as e:
        print(f'Ошибка записи файла в csv: {e}')
