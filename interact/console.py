import asyncio
import re

from playwright.sync_api import sync_playwright

from cloak.settings import WARM_UP_SITE
from scraper.product_article import ParserArticle
from scraper.product_parser import ProductParser

MAX_PARALLEL = 4


def get_total_products(url: str) -> int:
    """ Получение кол-ва продуктов """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
            )
            context.add_init_script("""
                                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                            """)
            page = context.new_page()
            page.goto(url, wait_until='networkidle', timeout=30_000)

            page.wait_for_selector('body', timeout=30_000)
            text = page.text_content('body')
            browser.close()
        except Exception as e:
            print(e)

    match = re.search(r'\d{1,3}(?:\s\d{3})*\s(?:продукта|продуктов)', text, flags=re.I)
    if match:
        numbers = int(re.sub(r'\D', '', match.group(0)))
        return numbers


def articles_parser(pages):
    """ Перебор страниц и сохранение артикулов и ссылок """
    article_parser = ParserArticle()
    articles = {}
    for i in range(1, pages):
        url = f'https://goldapple.ru/parfjumerija?p={i}'

        pars_art = article_parser.get_articles(url)

        if pars_art is None or not pars_art:
            print(f'\nСтраница {i} пустая – завершаем сбор.')
            break

        articles.update(pars_art)

        print(f'\rОбработано страниц: {i}/{pages}, Собрано артикулов: {len(articles)}/{count_product}', end='',
              flush=True)
    print()

    print(f'Собрали артикулов: {len(articles)}')
    return articles


async def get_product(articles_dict):
    """ Ассинхронный перебор продуктов и вытягивание всей нужной информации из html """
    parser = ProductParser()
    semaphore = asyncio.Semaphore(MAX_PARALLEL)

    async def fetch_one(key: str, suffix: str):
        async with semaphore:
            product = await parser.get_product_info(key, f"{WARM_UP_SITE}{suffix}")
            return key, product

    coros = [fetch_one(k, v) for k, v in articles_dict.items()]
    total = len(coros)
    done = 0
    products = []

    for coro in asyncio.as_completed(coros):
        key, product = await coro
        done += 1
        if product:
            products.append(product)
        else:
            print(f"Не удалось собрать информацию о продукте {key}")

        print(f"\rСобрано данный о продуктах {len(products)}/{total}", end="", flush=True)

    return products
