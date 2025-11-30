import pytest

from unittest.mock import patch, MagicMock

from scraper.product_article import ParserArticle


HTML_WITH_ARTICLES = """
<html><body>
<div class="pfzwtN">
  <meta content="Article 1">
  <a href="/link1">link1</a>
</div>
<div class="pfzwtN">
  <meta content="Article 2">
  <a href="/link2">link2</a>
</div>
<div class="pfzwtN">
  <!-- сломанный блок без meta -->
  <a href="/broken">broken</a>
</div>
</body></html>
"""

HTML_NO_ARTICLES = """
<html><body>
<div class="something-else">no articles here</div>
</body></html>
"""

def mock_sync_playwright(mock_sp):
    cm = mock_sp.return_value
    cm.__enter__.return_value = object()
    cm.__exit__.return_value = False
    return cm.__enter__.return_value


def patches(html):
    fake_browser = MagicMock(name='browser')
    fake_context = MagicMock(name='context')

    patch_sync = patch('playwright.sync_api.sync_playwright')
    patch_launch = patch.object(ParserArticle, '_launch_browser', return_value=fake_browser)
    patch_context = patch.object(ParserArticle, '_create_context', return_value=fake_context)
    patch_navigate = patch.object(ParserArticle, '_navigate_to_site', return_value=html)

    return patch_sync, patch_launch, patch_context, patch_navigate, fake_browser, fake_context

def test_get_articles():
    parser = ParserArticle()
    patch_sync, patch_launch, patch_context, patch_navigate, fake_browser, fake_context = patches(HTML_WITH_ARTICLES)

    with patch_sync as mock_sp, patch_launch as mock_launch, \
        patch_context as mock_context, patch_navigate as mock_navigate:

        s_obj = mock_sync_playwright(mock_sp)
        result = parser.get_articles('http://goldapple.ru')
        assert result == {'Article 1': '/link1', 'Article 2': '/link2'}



