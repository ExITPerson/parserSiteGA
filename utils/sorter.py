import logging
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from typing import Dict, List


logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(
        'logs/product_article.log',
        encoding='utf-8',
        maxBytes=5*1024*1024,
        backupCount=3
    )
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def sorter_product(data: List[dict]) -> dict:
    """ Сортирует список товаров по типам """
    if data is None:
        logger.warning('Передан None вместо списка товаров')
        return None

    logger.debug('Поступило %d товаров для сортировки', len(data))
    try:
        grouped = defaultdict(list)

        for product in data:
            tp = product.get("product_type")
            if tp:
                grouped[tp].append(product)
                logger.debug('Товар "%s" добавлен в группу "%s"',
                             product.get("name", "<без имени>"), tp)

            else:
                logger.debug('Товар без product_type пропущен: %s', product)
                continue

        result = dict(grouped)
        logger.info('Сортировка завершена: %d различных типов', len(result))
        return result

    except Exception as e:
        logger.exception(f'Невалидный формат данных при сортировке товаров, ошибка {e}')


def sort_by_popularity(data: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """
    Сортирует каждый список товаров по popularity_coefficient по убыванию.
    None считается минимальным значением.
    """
    logger.debug("Начинаем сортировку по популярности, %d групп товаров", len(data))

    def key_fn(prod: dict) -> tuple:
        coef = prod.get("popularity_coefficient")
        return (coef is None, -float(coef) if coef is not None else 0.0)

    sorted_data = {type_: sorted(products, key=key_fn) for type_, products in data.items()}
    logger.info(
        "Сортировка по популярности завершена: %d групп обработано",
        len(sorted_data),
    )
    return sorted_data
