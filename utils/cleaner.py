import logging
from logging.handlers import RotatingFileHandler

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


def clean_cell(text: str) -> str:
    """ Убирает переносы строк и лишние пробелы """
    logger.info('Запуск clean_cell')
    if text is None:
        logger.debug('Текста не найдено')
        return ""

    result = str(text).replace("\n", " ").replace("\r", " ").strip()
    logger.debug('Текст отформатирован')
    return result
