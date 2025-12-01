import asyncio

from interact.console import get_total_products, articles_parser, get_product
from utils.file_io import save_json, save_csv
from utils.sorter import sorter_product, sort_by_popularity


def main() -> None:
    count_product = int(get_total_products('https://goldapple.ru/parfjumerija'))
    print(f'Найдено товаров: {count_product}')

    pages = int(count_product / 24) + 1
    articles_pars = articles_parser(pages, count_product)

    products = asyncio.run(get_product(articles_pars))

    products = sorter_product(products)
    end_products = sort_by_popularity(products)

    save_json(end_products)
    for key, value in end_products.items():
        save_csv(value, key)

    print('Программа завершила работу, файлы с данными сохранены в папках data/csv и data/json')


if __name__ == '__main__':
    main()
