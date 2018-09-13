import json
import requests
from requests.exceptions import ConnectionError
from cookiepool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


if __name__ == "__main__":
    import time
    while True:
        rep = requests.get('https://sycm.taobao.com/ucc/mc/notify/listNotify.json?groupCode=one_plat',
        headers={
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept': '/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'cookie': 'cookie2=14063a46f720c6a585bc25625d87a773'
        })
        print(rep.text)
        time.sleep(120)
