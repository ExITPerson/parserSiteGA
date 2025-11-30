import time

import requests
import stem
from stem import control

from cloak.settings import CONTROL_PORT, SOCKS_HOST, SOCKS_PORT


def new_tor_ip(wait: bool = True) -> None:
    """строит новую цепь Tor (вызывать ПЕРЕД каждым requests)"""
    with control.Controller.from_port(port=CONTROL_PORT) as ctl:
        ctl.authenticate()
        ctl.signal(stem.Signal.NEWNYM)
        if wait:
            time.sleep(ctl.get_newnym_wait())

def tor_proxy():
    """возвращает прокси-словарь для requests"""
    proxy = f"socks5://{SOCKS_HOST}:{SOCKS_PORT}"  # без h, без auth
    return {"http": proxy, "https": proxy}

def tor_get(url, **kw):
    """GET-запрос ЧЕРЕЗ ТОР + автоматическая смена IP"""
    new_tor_ip()                      # ← новая цепь
    return requests.get(url, proxies=tor_proxy(), **kw)