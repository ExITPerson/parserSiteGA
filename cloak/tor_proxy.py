import time

import requests
import stem

SOCKS_HOST = '127.0.0.1'
SOCKS_PORT = 9050
CONTROL_PORT = 9051


def new_tor_ip(wait: bool = True) -> None:
    """строит новую цепь Tor (вызывать ПЕРЕД каждым requests)"""
    with stem.control.Controller.from_port(port=CONTROL_PORT) as ctl:
        ctl.authenticate()
        ctl.signal(stem.Signal.NEWNYM)
        if wait:
            time.sleep(ctl.get_newnym_wait())

def tor_proxy():
    """возвращает прокси-словарь для requests"""
    return {'http':  f'socks5h://{SOCKS_HOST}:{SOCKS_PORT}',
            'https': f'socks5h://{SOCKS_HOST}:{SOCKS_PORT}'}

def tor_get(url, **kw):
    """GET-запрос ЧЕРЕЗ ТОР + автоматическая смена IP"""
    new_tor_ip()                      # ← новая цепь
    return requests.get(url, proxies=tor_proxy(), **kw)