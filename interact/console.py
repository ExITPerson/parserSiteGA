import asyncio
import re

from playwright.sync_api import sync_playwright

from cloak.settings import WARM_UP_SITE, MAX_PARALLEL
from scraper.product_article import ParserArticle
from scraper.product_parser import ProductParser


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


async def articles_parser(pages: int, count_product: int) -> dict:
    """ Перебор страниц и сохранение артикулов и ссылок """
    urls = [f'https://goldapple.ru/parfjumerija?p= {i}' for i in range(1, pages)]
    parser = ParserArticle()
    sem = asyncio.Semaphore(MAX_PARALLEL)
    articles = {}
    total_pages = len(urls)

    async def one_page(idx: int, url: str) -> tuple[int, list | None]:
        """ Возвращает (номер_страницы, список_артикулов)"""
        async with sem:
            res = await parser.get_articles(url)
        return idx, res

    done = 0
    empty_streak = 0
    for coro in asyncio.as_completed([one_page(i, u) for i, u in enumerate(urls, 1)]):
        idx, res = await coro
        done += 1

        if res is None:
            empty_streak += 1
            if empty_streak >= 50:
                print(f"\n10 пустых страниц подряд — останавливаемся на {idx}")
                break
            continue
        else:
            empty_streak = 0

        articles.update({art: link for art, link in res})

        print(
            f'\rОбработано страниц: {done}/{total_pages} | Артикулов: {len(articles)}/{count_product}',
            end='',
            flush=True
        )

    print()
    print('\nГотово. Всего артикулов:', len(articles))
    return articles


async def get_product(articles_dict: dict) -> list:
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
