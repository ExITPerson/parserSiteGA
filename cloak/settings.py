import os


PROXY = True # True используем прокси, False не используем прокси
FAKE_UA = True # True для использования фейкового User-Agent, False используем реальный User-Agent
TIMEOUT = 30_000 # Редактировать, при низкой скорости интернета

# Дефолтные значения, не редактировать
WARM_UP_SITE = 'https://goldapple.ru'
TOR_EXE_PATH = os.getenv('TOR_PATH') # Путь до файла tor.exe
DEFAULT_ACCEPT = 'application/json, text/plain, */*'
SOCKS_HOST = "127.0.0.1"
SOCKS_PORT = 9050
CONTROL_PORT = 9051