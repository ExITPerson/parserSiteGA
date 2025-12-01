import asyncio
from typing import Dict

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from cloak.fakeua import random_ua
from cloak.settings import TIMEOUT, FAKE_UA


class ProductParser:
    def __init__(self):
        self._viewport = {"width": 1280, "height": 720}
        self._timeout = TIMEOUT

    async def get_product_info(self, key: str, url: str) -> Dict[str, str | None | float]:
        async with async_playwright() as p:
            browser = await self._launch_browser(p)

            try:
                context = await self._create_context(browser)
                html = await self._navigate_to_site(context, url)
                soup = BeautifulSoup(html, "lxml")

                name = (n.text.strip() if (n := soup.find("div", {"text": "Описание"})) and
                                          (n := n.find("div", class_="EYSKW2")) else "")
                rating = (r["content"] if (r := soup.find("div", class_="N3JFDN")) and
                                          (r := r.find_next()) else 1)
                review = (r2["content"] if (r := soup.find("div", class_="N3JFDN")) and
                                           (r2 := r.find_next().find_next()) else 1)
                popularity_coefficient = round((((float(rating) / 5) * (int(review) / 1000)) * 1000), 2)
                type_product = (t.text.strip() if (t := soup.find("dt", class_="_1xOE3E")) else "")
                description = (d.text.strip() if (d := soup.find("div", class_="ihiTqq")) else "")

                country = ""
                if (block := soup.find("div", {"text": "Дополнительная информация"})):

                    if (b := block.select_one("div.ihiTqq")):
                        tmp = b.get_text(strip=True, separator=" ")
                        country = tmp.split("страна происхождения")[1].split("изготовитель")[0].strip() \
                            if "страна происхождения" in tmp and "изготовитель" in tmp else ""

                application = (a.text.strip() if (a := soup.find("div", {"text": "Применение"})) else "")

                all_price = soup.find_all("div", class_="_4E8GKT +VtqAS")
                price = "".join(i for i in all_price[0].text.strip() if i.isdigit()) if all_price else ""
                sale_price = "".join(i for i in all_price[1].text.strip() if i.isdigit()) if len(all_price) > 1 else ""

                return {
                    'article': key,
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

            except Exception as exc:
                print(f"Ошибка при парсинге {url}: {exc}")
                return {}

            finally:
                try:
                    await browser.close()

                except Exception:
                    pass

    async def _launch_browser(self, playwright):
        return await playwright.chromium.launch(
            headless=True,
            slow_mo=50,
        )

    async def _create_context(self, browser):
        context = await browser.new_context(
            viewport=self._viewport,
            user_agent=random_ua() if FAKE_UA else None
        )
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        """)
        return context

    async def _navigate_to_site(self, context, url: str) -> str:
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector("div.Gl9aTE", timeout=self._timeout)

        t0 = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - t0 < 20:
            before = await page.locator("div.Gl9aTE").count()
            await page.wait_for_timeout(1500)
            after = await page.locator("div.Xk-cI1").count()

            if before != after:
                break

        return await page.content()

