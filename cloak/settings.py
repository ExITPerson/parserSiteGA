import os

FAKE_UA = True if os.getenv('FAKE_UA') == 'True' else False # True для использования фейкового User-Agent, False используем реальный User-Agent
TIMEOUT = os.getenv('TIMEOUT') # Редактировать, при низкой скорости интернета

# Дефолтные значения, не редактировать
WARM_UP_SITE = os.getenv('WARM_UP_SITE')
DEFAULT_ACCEPT = os.getenv('DEFAULT_ACCEPT')