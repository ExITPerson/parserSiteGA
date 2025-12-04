import logging
from logging.handlers import RotatingFileHandler

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from utils.fakeua import random_ua
from cloak.settings import TIMEOUT, FAKE_UA


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


class ParserArticle:
    def __init__(self):
        self._viewport = {"width": 1280, "height": 720}
        self._proxy = None
        self._timeout = TIMEOUT

    async def get_articles(self, url: str) -> list | None:
        logger.debug(f'URL для парсинга: {url}')
        async with async_playwright() as p:
            browser = await self._launch_browser(p)
            try:
                context = await self._create_context(browser)
                html = await self._navigate_to_site(context, url)
            except Exception as e:
                logger.exception(f'Ошибка в блоке get_articles: {e}')
                html = None
            finally:
                logger.info('Закрываем браузер для экономии')
                await browser.close()

        if html is None:
            logger.info('Html контента не обнаружено отдаем None')
            return None

        logger.debug('Получен html %d байт', len(html))
        soup = BeautifulSoup(html, 'lxml')
        blocks = soup.find_all('div', class_='pfzwtN')
        if not blocks:
            logger.warning('Нужного нам блока на странице нет, URL: %s', url)
            return None
        logger.debug(f'Кол-во найденных блоков: {len(blocks)}')

        articles = {}
        for bl in blocks:
            try:
                art = bl.find('meta')['content']
                link = bl.find('a')['href']
                articles[art] = link
            except Exception:
                logger.debug('Нужных блоков не найдено')
                continue
        logger.info(f'Отдаем словарь с артикулами: {len(articles)}')
        return list(articles.items())

    async def _launch_browser(self, playwright):
        logger.info('Открываем браузер')
        return await playwright.chromium.launch(
            headless=True,
            slow_mo=50,
            proxy=self._proxy
        )

    async def _create_context(self, browser):
        logger.info('Создаем контекст с настройками')
        ctx = await browser.new_context(
            viewport=self._viewport,
            proxy=self._proxy,
            user_agent=random_ua() if FAKE_UA else None
        )
        logger.info('Добавляем скрипт для обхода антибота')
        await ctx.add_init_script("""
               Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
               Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
           """)
        return ctx

    async def _navigate_to_site(self, context, url):
        logger.info('Грузим страницу, дожидаемся появления нужного нам элемента.')
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        try:
            logger.info('Ждем появления элемента')
            await page.wait_for_selector("div.pfzwtN", timeout=self._timeout)
        except Exception:
            logger.info('Элемент не прогрузился, отдаем появившийся контент')
            return await page.content()

        logger.info('Ждем появления всех нужных нам артикулов в html страницы')
        attempts = 0
        while attempts < 3:
            before = await page.locator("div.pfzwtN").count()
            await page.wait_for_timeout(1500)
            after = await page.locator("div.pfzwtN").count()
            if before == after:
                break
            attempts += 1
        logger.info('Нужная нам информация прогрузилась, отдаем html')
        return await page.content()
