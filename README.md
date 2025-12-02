# 🌟 parserSiteGA  
![Logo](./assets/логотип.jpg)

> Умный парсер раздела парфюмерии с сайта [goldapple.ru](https://goldapple.ru/parfjumerija), который собирает данные о товарах, сортирует их по популярности и сохраняет в удобные CSV и JSON файлы.  
Идеально подходит для анализа спроса, закупок и маркетинговых стратегий.

---

## 📌 Оглавление
- [📖 Описание](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5)
- [🚀 Возможности](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D0%B2%D0%BE%D0%B7%D0%BC%D0%BE%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D0%B8)
- [🧰 Технологии](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8)
- [⚙️ Установка](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#%EF%B8%8F-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0)
- [🧪 Тестирование](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)
- [🧬 Структура проекта](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0)
- [⚙️ Конфигурация](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#%EF%B8%8F-%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%D1%83%D1%80%D0%B0%D1%86%D0%B8%D1%8F)
- [🕹 Использование](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)
- [📈 Производительность](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C)
- [📬 Контакты](https://github.com/ExITPerson/parserSiteGA/tree/feature/start_parser_project?tab=readme-ov-file#-%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D1%8B)

---

## 📖 Описание
`parserSiteGA` — это парсер, разработанный для сбора и анализа данных о парфюмерных товарах с сайта GoldApple.  
Проект автоматизирует процесс сбора информации: от артикулов и цен до рейтингов и описаний.  
Все данные структурируются по типу продукта и сортируются по **коэффициенту популярности**, что позволяет легко определить трендовые позиции.

---

## 🚀 Возможности
- 📦 Парсинг всех товаров раздела «Парфюмерия»
- 🔢 Автоматический расчёт популярности на основе рейтинга и количества отзывов
- 📊 Сохранение результатов в `CSV` и `JSON`
- 🧹 Очистка и структурирование данных
- ⚙️ Настраиваемые параметры парсинга
- 🧪 Покрытие тестами
- 🧠 Асинхронная архитектура для высокой скорости

---

## ✅ Примеры файлов CSV и JSON

- [CSV Файл с результатами](./data/csv/2025-12-02_туалетная вода.csv)
- [JSON Файл с результатами](./data/json/2025-12-02_products.json)

---

## 🧰 Технологии
- **Python 3.11+**
- **Playwright** — для эмуляции браузера и рендеринга страниц
- **BeautifulSoup4 + lxml** — для парсинга HTML
- **asyncio** — для асинхронной обработки
- **pytest + coverage** — для тестирования
- **flake8** — для проверки кода по стандарту PEP8

---

## ⚙️ Установка

### 1. Клонирование репозитория
```bash
git clone git@github.com:ExITPerson/parserSiteGA.git
cd parserSiteGA
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Установка Playwright браузеров
```bash
playwright install
```

---

## 🧪 Тестирование

### Запуск тестов с покрытием:
```bash
pytest --cov
```
> [📊 Открыть детальную информацию о тестах](./htmlcov/index.html)

---

## 🧬 Структура проекта

```
parserSiteGA/
├── cloak/                  # Конфигурации и утилиты
│   └── settings.py         # Настройки парсинга
├── interact/               # Логика взаимодействия
│   └── console.py          # Консольный интерфейс
├── scraper/                # Парсеры
│   ├── product_article.py  # Сбор артикулов
│   └── product_parser.py   # Сбор данных о товаре
├── utils/                  # Утилиты
│   ├── cleaner.py          # Очистка текста
│   ├── file_io.py          # Сохранение в CSV/JSON
│   ├── fakeua.py           # Генерация User-Agent
│   └── sorter.py           # Сортировка по популярности
├── tests/                  # Тесты
│   ├── test_parser_product.py
│   ├── test_sorter.py
│   ├── test_parser_article.py
│   ├── test_cleaner.py
│   └── test_file_io.py
├── data/                   # Сохранённые результаты
│   ├── csv/
│   └── json/
├── main.py                 # Точка входа
├── requirements.txt
├── .flake8
├── .gitignore
└── README.md
```

---


### ⚙️ Конфигурация
Все регулировки — в файле `cloak/settings.py`:

| Параметр            | Значение по умолчанию | Описание |
|---------------------|------------------------|----------|
| `FAKE_UA`           | `False`                | `True` → использовать случайный фейковый User-Agent |
| `TIMEOUT`           | `120_000` мс           | Максимальное время ожидания загрузки страницы |
| `WARM_UP_SITE`      | `https://goldapple.ru` | Базовый URL (не редактировать) |
| `MAX_PARALLEL`      | `4`                    | Количество одновременных браузеров  |

> ⚠️ При медленном интернете увеличь `TIMEOUT`, а при блокировке IP — включите `FAKE_UA = True` и используйте PROXY.

---

## 🕹 Использование
```bash
python main.py
```

### Программа:
- Определит количество товаров
- Соберёт артикулы и ссылки
- Парсит данные о каждом товаре
- Сгруппирует по типу и отсортирует по популярности
- Сохранит всё в data/csv/ и data/json/

---

## 📈 Производительность
- Асинхронная обработка до 4 потоков одновременно
- Возможность расширения до многопроцессорности при деплое на мощные серверы (рекомендация)

---

### 📬 Контакты
**Автор:** ExITPerson  
**GitHub:** [github.com/ExITPerson](https://github.com/ExITPerson)

> 💡 Если у вас есть идеи по улучшению или вопросы — открывайте [issue](https://github.com/ExITPerson/parserSiteGA/issues) или пишите в [дискуссии](https://github.com/ExITPerson/parserSiteGA/discussions)!

---

> 💬 *"Кто владеет данными — владеет рынком."*  
> `parserSiteGA` помогает быть на шаг впереди.
