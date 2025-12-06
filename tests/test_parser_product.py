import pytest

from unittest.mock import patch, MagicMock, AsyncMock

from scraper.product_parser import ProductParser


HTML_PRODUCT = """
<html>
<body>
    <div text="Описание">
        <div class="EYSKW2"> Очень крутой продукт </div>
    </div>

    <div class="N3JFDN"></div>
    <meta content="4.5"></meta>
    <meta content="200"></meta>

    <dt class="_1xOE3E">Супер-шампунь</dt>
    <div class="ihiTqq">Описание товара тут</div>

    <div text="Дополнительная информация">
        <div class="ihiTqq">
            всякое-всякое страна происхождения Россия изготовитель ООО "Рога и Копыта"
        </div>
    </div>

    <div text="Применение">Наносить на волосы один раз в день</div>

    <div class="_4E8GKT +VtqAS">1 234 ₽</div>
    <div class="_4E8GKT +VtqAS">999 ₽</div>
</body>
</html>
"""


@pytest.mark.asyncio
async def test_get_product_info_success():
    parser = ProductParser()
    fake_browser = MagicMock(name="browser")
    fake_browser.close = AsyncMock()
    fake_context = MagicMock(name="context")

    with patch(
        "playwright.async_api.async_playwright", new_callable=AsyncMock
    ) as mock_async_playwright, patch.object(
        ProductParser, "_launch_browser", new_callable=AsyncMock
    ) as mock_launch, patch.object(
        ProductParser, "_create_context", new_callable=AsyncMock
    ) as mock_create_ctx, patch.object(
        ProductParser, "_navigate_to_site", new_callable=AsyncMock
    ) as mock_nav:

        playwright_obj = object()
        cm = AsyncMock()
        cm.__aenter__.return_value = playwright_obj
        cm.__aexit__.return_value = False
        mock_async_playwright.return_value = cm

        mock_launch.return_value = fake_browser
        mock_create_ctx.return_value = fake_context
        mock_nav.return_value = HTML_PRODUCT

        result = await parser.get_product_info(
            "ABC123", "https://goldapple.com/product"
        )

    expected = {
        "article": "ABC123",
        "name": "Очень крутой продукт",
        "product_type": "Супер-шампунь",
        "country": "Россия",
        "price_actual": "1234",
        "price_loyalty": "999",
        "url": "https://goldapple.com/product",
        "popularity_coefficient": 180.0,
        "description": "Описание товара тут",
        "application": "Наносить на волосы один раз в день",
    }

    assert result == expected
