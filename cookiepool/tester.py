# -*- coding: utf-8 -*-
import json

import requests

from cookiepool.db import *


class ValidTester(object):
    def __init__(self, shop='default'):
        self.shop = shop
        self.cookies_db = RedisClient(self.shop, 'cookies')
        self.accounts_db = RedisClient(self.shop, 'accounts')

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class taobaoValidTester(ValidTester):
    def __init__(self, shop='pechoin'):
        ValidTester.__init__(self, shop)

    def test(self, username, cookies):
        print('detect {}'.format(username))
        cookie = json.loads(cookies, encoding='utf-8')
        cookie2 = cookie.get('cookie2', None)
        csg = cookie.get('csg', None)
        rep = requests.get('https://sycm.taobao.com/portal/live/overview.json',
                           headers={
                               'Connection': 'keep-alive',
                               'Cache-Control': 'max-age=0',
                               'Accept': '/',
                               'Upgrade-Insecure-Requests': '1',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
                               'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': 'zh-CN,zh;q=0.8',
                               'cookie': 'cookie2={cookie2}; csg={csg}'.format(cookie2=cookie2, csg=csg)
                           })
        if rep.status_code == 200:
            rep = json.loads(rep.text, encoding='utf-8')
            if rep.get('code', None) == 5810:
                print('delete cookie {}'.format(username))
                self.cookies_db.delete(username)


if __name__ == "__main__":
    ss = taobaoValidTester(shop='pechoin')
    ss.run()
