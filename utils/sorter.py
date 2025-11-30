from collections import defaultdict
from typing import Dict, List


def sorter_product(data):
    """ Сортирует список товаров по типам """
    grouped = defaultdict(list)

    for product in data:
        tp = product.get("product_type")
        grouped[tp].append(product)

    return dict(grouped)

def sort_by_popularity(data: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """
    Сортирует каждый список товаров по popularity_coefficient по убыванию.
    None считается минимальным значением.
    """
    def key_fn(prod: dict) -> tuple:

        coef = prod.get("popularity_coefficient")
        return (coef is None, -float(coef) if coef is not None else 0.0)

    return {type_: sorted(products, key=key_fn) for type_, products in data.items()}

