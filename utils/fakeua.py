from fake_useragent import UserAgent


def random_ua() -> str:
    return UserAgent(platforms="desktop").random
