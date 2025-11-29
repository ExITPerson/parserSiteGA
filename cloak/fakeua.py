from fake_useragent import UserAgent

def random_ua():
    return UserAgent(platforms='desktop').random