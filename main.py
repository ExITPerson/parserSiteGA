import asyncio
import re

from playwright.sync_api import sync_playwright

from cloak.settings import WARM_UP_SITE
from scraper.product_article import ParserArticle
from scraper.product_parser import ProductParser
from utils.file_io import save_json, save_csv
from utils.sorter import sorter_product, sort_by_popularity


def get_total_products(url: str) -> int:
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
        numbers = int(re.sub(r'\D', '', match.group(0)))  # 19117
        return numbers

def articles_parser(pages):
    article_parser = ParserArticle()
    articles = {}
    for i in range(1, 3):
        url = f'https://goldapple.ru/parfjumerija?p={i}'

        pars_art = article_parser.get_articles(url)

        if pars_art is None:  # ← пустая страница
            print(f'\nСтраница {i} пустая – завершаем сбор.')
            break

        articles.update(pars_art)

        print(f'\rОбработано страниц: {i}/{pages}, Собрано артикулов: {len(articles)}/{count_product}', end='',
              flush=True)

    print()
    print(articles)

    print(f'Собрали артикулов: {len(articles)}')
    return articles

MAX_PARALLEL = 4

async def main(articles_dict):
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

if __name__ == '__main__':
    count_product = int(get_total_products('https://goldapple.ru/parfjumerija'))

    print(f'Найдено товаров: {count_product}')

    pages = int(count_product / 24) + 1
    articles_pars = articles_parser(pages)
    # articles_pars = {'19000312616': '/19000312616-private-anthem', '99000079532': '/99000079532-cernyj', '19000166818': '/19000166818-blockade', '19000235935': '/19000235935-guidance', '19000391661': '/19000391661-pulsation-11-07', '19000238659': '/19000238659-spontaneous-generosity', '26166000003': '/26166000003-starry-night', '19000148353': '/19000148353-bois-imperial-by-quentin-bisch', '19000163469': '/19000163469-bendito-beso', '99000047786': '/99000047786-hide-me', '80284600002': '/80284600002-man-wood-essence', '99000009838': '/99000009838-paolo-01', '19000253144': '/19000253144-wildbloom-vert', '19760303655': '/19760303655-baccarat-rouge-540', '99000027997': '/99000027997-valentina-you-are-so-cupid', '19000370747': '/19000370747-the-scent', '19000222826': '/19000222826-imperiale-vanille-malika', '19000005046': '/19000005046-aire-sutileza', '7430500001': '/7430500001-eau-fraiche', '63620400001': '/63620400001-imperial', '99000048387': '/99000048387-descovery-set', '19000206599': '/19000206599-mornings-in-milano', '19000288455': '/19000288455-one-only', '19760300405': '/19760300405-501-praline-reglisse-patchouli', '19000359497': '/19000359497-irresistible', '99000047788': '/99000047788-unleash', '19000257719': '/19000257719-conquer-me', '26730600002': '/26730600002-bal-d-afrique', '99000009839': '/99000009839-quentin-03', '19000244569': '/19000244569-momento', '7233900001': '/7233900001-guilty-pour-femme', '99000021901': '/99000021901-tobacco-vanilla',}

    products = asyncio.run(main(articles_pars))
    print(type(products))

    products = sorter_product(products)

    end_products = sort_by_popularity(products)

    save_json(end_products)
    for key, value in end_products.items():
        save_csv(value, key)

