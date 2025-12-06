import asyncio
import logging
import re
from logging.handlers import RotatingFileHandler
from typing import Dict

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from utils.fakeua import random_ua
from cloak.settings import TIMEOUT, FAKE_UA


logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(
        "logs/product_article.log", encoding="utf-8", backupCount=3
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


class ProductParser:
    def __init__(self) -> None:
        self._viewport = {"width": 1280, "height": 720}
        self._timeout = TIMEOUT

    async def get_product_info(
        self, key: str, url: str
    ) -> Dict[str, str | None | float]:
        logger.debug(f"URL для парсинга: {url}")
        async with async_playwright() as p:
            browser = await self._launch_browser(p)

            try:
                context = await self._create_context(browser)
                html = await self._navigate_to_site(context, url)
                logger.debug("Получен html %d байт", len(html))
                soup = BeautifulSoup(html, "lxml")

                logger.info("Получаем нужную нам информацию из html")
                brand = (
                    n.text.strip()
                    if (n := soup.find("div", {"text": "Бренд"}))
                    and (n := n.find("div", class_="Y7lj03"))
                    else ""
                )
                name = (
                    n.text.strip()
                    if (n := soup.find("div", {"text": "Описание"}))
                    and (n := n.find("div", class_="Y7lj03"))
                    else ""
                )
                rating = (
                    r["content"]
                    if (r := soup.find("div", class_="L4oxGP")) and (r := r.find_next())
                    else 1
                )
                review = (
                    r2["content"]
                    if (r := soup.find("div", class_="L4oxGP"))
                    and (r2 := r.find_next().find_next())
                    else 1
                )
                popularity_coefficient = round(
                    (((float(rating) / 5) * (int(review) / 1000)) * 1000), 2
                )
                type_product = (
                    t.text.strip() if (t := soup.find("dt", class_="KI1Mtc")) else ""
                )
                description = (
                    d.text.strip() if (d := soup.find("div", class_="_4xzZIg")) else ""
                )

                country = (
                    re.search(
                        r"страна происхождения\s*[:–\-]?\s*(.+?)"
                        r"(?:\sизготовитель|\bпрочие|\bсостав|\bупаковка|\sпродавец|$)",
                        soup.find(
                            "div", {"text": "Дополнительная информация"}
                        ).get_text(" ", strip=True),
                        flags=re.I,
                    )
                    .group(1)
                    .strip()
                )

                application = (
                    a.text.strip()
                    if (a := soup.find("div", {"text": "Применение"}))
                    else ""
                )

                all_price = soup.find_all("div", class_="_9ouGkW _55FAYu")
                price = (
                    "".join(i for i in all_price[0].text.strip() if i.isdigit())
                    if all_price
                    else ""
                )
                sale_price = (
                    "".join(i for i in all_price[1].text.strip() if i.isdigit())
                    if len(all_price) > 1
                    else ""
                )

                logger.info("Всю информацию получили, отдаем словарь")
                return {
                    "article": key,
                    "brand": brand or None,
                    "name": name or None,
                    "product_type": type_product or None,
                    "country": country or None,
                    "price_actual": price or None,
                    "price_loyalty": sale_price or None,
                    "url": url,
                    "popularity_coefficient": popularity_coefficient or None,
                    "description": description or None,
                    "application": application or None,
                }

            except Exception as e:
                logger.exception(f"Ошибка в блоке get_articles: {e}, URL: %s", url)
                return {}

            finally:
                try:
                    logger.info("Закрываем браузер")
                    await browser.close()

                except Exception:
                    logger.info("Браузер не закрыт, заглушка")
                    pass

    async def _launch_browser(self, playwright) -> None:
        logger.info("Открываем браузер")
        return await playwright.chromium.launch(
            headless=True,
            slow_mo=50,
        )

    async def _create_context(self, browser) -> object:
        logger.info("Создаем контекст с настройками")
        context = await browser.new_context(
            viewport=self._viewport, user_agent=random_ua() if FAKE_UA else None
        )
        logger.info("Добавляем скрипт для обхода антибота")
        await context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        """
        )
        return context

    async def _navigate_to_site(self, context, url: str) -> str:
        logger.info("Грузим страницу, дожидаемся появления нужного нам элемента.")
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        try:
            logger.info("Ждем появления элемента")
            await page.wait_for_selector("div.GmM9E2", timeout=self._timeout)

        except Exception:
            logger.info("Элемент не прогрузился, отдаем появившийся контент")
            return await page.content()

        logger.info("Ждем появления всей нужной нам информации в html странице")
        t0 = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - t0 < 20:
            before = await page.locator("div.GmM9E2").count()
            await page.wait_for_timeout(1500)
            after = await page.locator("div.XfuK-b").count()

            if before != after:
                break

        logger.info("Нужная нам информация прогрузилась, отдаем html")
        return await page.content()
