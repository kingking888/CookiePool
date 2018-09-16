# -*- coding: utf-8 -*-
import json
from flask import Flask, g
from cookiepool.config import *
from cookiepool.db import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    获取
    :return:
    """
    for shop in GENERATOR_MAP:
        print(shop)
        if not hasattr(g, shop):
            setattr(g, shop + '_cookies', eval('RedisClient' + '("' + shop + '", "cookies")'))
            setattr(g, shop + '_accounts', eval('RedisClient' + '("' + shop + '","accounts")'))
    return g


@app.route('/<shop>/random')
def random(shop):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = get_conn()
    cookies = getattr(g, shop + '_cookies').random()
    return cookies


@app.route('/<shop>/add/<username>/<password>')
def add(shop, username, password):
    """
    添加用户, 访问地址如 /shop/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return:
    """
    g = get_conn()
    print(username, password)
    getattr(g, shop + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<shop>/count')
def count(shop):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, shop + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


@app.route('/<shop>/delcookie/<cookie>')
def del_cookie(shop, cookie):
    """
    删除cookie, 访问地址如 /shop/delcookie/cookie/
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return:
    """
    g = get_conn()
    cookie_db = getattr(g, shop + '_cookies')
    cookie_maps = cookie_db.all()
    status = None
    if cookie_maps:
        for k,v in cookie_maps.items():
            cookie_dict = json.loads(v,encoding='utf-8')
            if cookie_dict['cookie2'] == cookie:
                status = cookie_db.delete(k)

    return json.dumps({'status': status, 'res': cookie_db.random()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)