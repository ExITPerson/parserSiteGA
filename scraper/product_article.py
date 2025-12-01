import time

from bs4 import BeautifulSoup
from playwright.async_api import Page
from playwright.sync_api import sync_playwright

from utils.fakeua import random_ua
from cloak.settings import TIMEOUT, FAKE_UA


class ParserArticle:
    def __init__(self) -> None:
        self._viewport = {"width": 1280, "height": 720}
        self._timeout = TIMEOUT

    def get_articles(self, url: str) -> list | None:
        with sync_playwright() as s:
            browser = self._launch_browser(s)

            try:
                context = self._create_context(browser)
                html = self._navigate_to_site(context, url)
                soup = BeautifulSoup(html, 'lxml')
                articles_block = soup.find_all('div', class_='pfzwtN')

                if not articles_block:
                    return

                articles = {}
                for art in articles_block:
                    try:
                        article = art.find('meta')['content']
                        link = art.find('a')['href']
                        articles[article] = link

                    except Exception:
                        continue

                if not articles:
                    return None

                return articles

            except Exception as e:
                print(f'Ошибка в блоке get_articles: {e}')

            except Page.wait_for_selector:
                return None

            finally:
                try:
                    browser.close()
                except Exception:
                    pass

    def _launch_browser(self, playwright) -> None:
        return playwright.chromium.launch(
            headless=True,
            slow_mo=50,
        )

    def _create_context(self, browser) -> object:
        context = browser.new_context(
            viewport=self._viewport,
            user_agent=random_ua() if FAKE_UA else None
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        """)
        return context

    def _navigate_to_site(self, context, url: str) -> str:
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("div.pfzwtN", timeout=self._timeout)

        t0 = time.time()
        while time.time() - t0 < 20:
            before = page.locator("div.pfzwtN").count()
            page.wait_for_timeout(1500)
            after = page.locator("div.pfzwtN").count()

            if before == after:
                break

        return page.content()
