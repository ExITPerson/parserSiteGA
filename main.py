import asyncio
import re

from playwright.sync_api import sync_playwright

from scraper.product_article import ParserArticle


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

def main(pages):
    article_parser = ParserArticle()
    articles = {}
    for i in range(1, pages):
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

if __name__ == '__main__':
    count_product = int(get_total_products('https://goldapple.ru/parfjumerija'))

    print(f'Найдено товаров: {count_product}')

    pages = int(count_product / 20) + 1
    main(pages)