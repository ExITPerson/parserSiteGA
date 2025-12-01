from collections import defaultdict
from typing import Dict, List


def sorter_product(data: List[dict]) -> dict:
    """ Сортирует список товаров по типам """
    try:
        grouped = defaultdict(list)

        for product in data:
            if product.get("product_type"):
                tp = product.get("product_type")
                grouped[tp].append(product)

            else:
                continue

        return dict(grouped)

    except Exception as e:
        print(f'Передан не верный формат данных: {e}')


def sort_by_popularity(data: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """
    Сортирует каждый список товаров по popularity_coefficient по убыванию.
    None считается минимальным значением.
    """
    def key_fn(prod: dict) -> tuple:

        coef = prod.get("popularity_coefficient")
        return (coef is None, -float(coef) if coef is not None else 0.0)

    return {type_: sorted(products, key=key_fn) for type_, products in data.items()}
