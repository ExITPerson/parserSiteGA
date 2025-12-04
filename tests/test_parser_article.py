import pytest
from unittest.mock import AsyncMock, MagicMock

from cloak.settings import TIMEOUT
from scraper.product_article import ParserArticle   # замените на реальный путь


def test_default_init():
    p = ParserArticle()
    assert p._viewport == {"width": 1280, "height": 720}
    assert p._proxy is None
    assert p._timeout == TIMEOUT


@pytest.mark.asyncio
async def test_launch_browser(monkeypatch):
    p = ParserArticle()

    fake_browser = MagicMock()
    launch_mock = AsyncMock(return_value=fake_browser)
    monkeypatch.setattr("playwright.async_api.async_playwright", AsyncMock(
        return_value=MagicMock(chromium=MagicMock(launch=launch_mock))
    ))

    async with AsyncMock() as pw:
        pw.chromium.launch = launch_mock
        browser = await p._launch_browser(pw)

    launch_mock.assert_awaited_once_with(headless=True, slow_mo=50, proxy=None)
    assert browser is fake_browser


@pytest.mark.asyncio
async def test_create_context(monkeypatch):
    p = ParserArticle()

    fake_ctx = MagicMock()
    fake_ctx.add_init_script = AsyncMock()

    new_ctx_mock = AsyncMock(return_value=fake_ctx)
    browser = MagicMock(new_context=new_ctx_mock)

    ctx = await p._create_context(browser)

    new_ctx_mock.assert_awaited_once_with(
        viewport=p._viewport,
        proxy=None,
        user_agent=None
    )
    fake_ctx.add_init_script.assert_awaited_once()
    assert ctx is fake_ctx


@pytest.mark.asyncio
async def test_navigate_to_site(monkeypatch):
    p = ParserArticle()

    page_mock = MagicMock()
    page_mock.goto = AsyncMock()
    page_mock.wait_for_selector = AsyncMock()
    page_mock.wait_for_timeout = AsyncMock()
    locator_mock = MagicMock(count=AsyncMock(side_effect=[5, 5]))
    page_mock.locator = MagicMock(return_value=locator_mock)
    page_mock.content = AsyncMock(return_value="<html></html>")

    context_mock = MagicMock(new_page=AsyncMock(return_value=page_mock))

    html = await p._navigate_to_site(context_mock, "http://test")

    page_mock.goto.assert_awaited_once_with("http://test", wait_until="domcontentloaded")
    page_mock.wait_for_selector.assert_awaited_once_with("div.pfzwtN", timeout=p._timeout)
    assert html == "<html></html>"


@pytest.mark.asyncio
async def test_get_articles_success(monkeypatch):
    p = ParserArticle()

    fake_html = """
    <html>
      <div class="pfzwtN">
        <meta content="12345"/>
        <a href="/product/12345"/>
      </div>
      <div class="pfzwtN">
        <meta content="67890"/>
        <a href="/product/67890"/>
      </div>
    </html>
    """

    monkeypatch.setattr(p, "_navigate_to_site", AsyncMock(return_value=fake_html))
    monkeypatch.setattr(p, "_launch_browser", AsyncMock())
    monkeypatch.setattr(p, "_create_context", AsyncMock())

    # чтобы не закрывать реальный браузер
    fake_browser = MagicMock(close=AsyncMock())
    monkeypatch.setattr(p, "_launch_browser", AsyncMock(return_value=fake_browser))

    articles = await p.get_articles("http://test")

    assert articles is not None
    assert len(articles) == 2
    assert ("12345", "/product/12345") in articles
    assert ("67890", "/product/67890") in articles


@pytest.mark.asyncio
async def test_get_articles_no_blocks(monkeypatch):
    p = ParserArticle()

    fake_html = "<html><body>Пусто</body></html>"

    monkeypatch.setattr(p, "_navigate_to_site", AsyncMock(return_value=fake_html))
    fake_browser = MagicMock(close=AsyncMock())
    monkeypatch.setattr(p, "_launch_browser", AsyncMock(return_value=fake_browser))
    monkeypatch.setattr(p, "_create_context", AsyncMock())

    articles = await p.get_articles("http://test")

    assert articles is None


@pytest.mark.asyncio
async def test_get_articles_site_fail(monkeypatch):
    p = ParserArticle()

    monkeypatch.setattr(p, "_navigate_to_site", AsyncMock(return_value=None))
    fake_browser = MagicMock(close=AsyncMock())
    monkeypatch.setattr(p, "_launch_browser", AsyncMock(return_value=fake_browser))
    monkeypatch.setattr(p, "_create_context", AsyncMock())

    articles = await p.get_articles("http://bad")

    assert articles is None