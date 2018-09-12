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
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random_cookie(website):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').s_get_random()
    return cookies


@app.route('/<website>/delete/<cookie>')
def all(website,cookie):
    """
    获取Cookies总数
    """
    g = get_conn()
    all = getattr(g, website + '_cookies').s_del(cookie)
    return json.dumps({'status': '1', 'cookie': all})


@app.route('/<website>/all')
def all(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    all = getattr(g, website + '_cookies').s_all()
    return json.dumps({'status': '1', 'count': all})


if __name__ == '__main__':
    app.run(host='127.0.0.0')