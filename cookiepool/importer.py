# -*- coding: utf-8 -*-
import requests

from cookiepool.db import RedisClient



def set(account, sep='----'):
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组, 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    shop = input("请输入店铺名")
    conn = RedisClient('pechoin' , 'accounts')
    scan()
