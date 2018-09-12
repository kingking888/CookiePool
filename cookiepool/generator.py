import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cookiepool.config import *
from cookiepool.db import RedisClient
import requests
import logging

logger = logging.getLogger(__name__)


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.website = website
        self.cookies_db = RedisClient(self.website,'cookies')
        self.accounts_db = RedisClient(self.website,'accounts')
        self.browser = webdriver.Chrome()

    def __del__(self):
        self.close()

    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()
        for username in accounts_usernames:
            if not username in cookies_usernames:
                print('正在生成Cookies', '账号', username)
                cookies = self.new_cookies(username,password=None)
                # 成功获取
                if cookies:
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.s_set(cookies):
                        print('成功保存Cookies')
                else:
                    print('错误result{}'.format(cookies))

    def close(self):
        """
        关闭
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class taobaoCookiesGenerator(CookiesGenerator):
    login_address = "https://login.taobao.com/member/login.jhtml"
    server_address = "http://120.55.113.9:8080/spider-server/web/api/loginQrCode"
    success_address = "https://mai.taobao.com/seller_admin.htm"
    refrash_loc = "document.querySelector('.J_QRCodeRefresh').click()"

    def __init__(self, website='taobao'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, website)
        super()
        self.website = website

    def new_cookies(self, username, password=None):
        """
         初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        self.browser.get(self.login_address)
        # 获取当前的cookie
        cookie = self.browser.get_cookie('cookie2')
        if cookie:
            count = 0
            while self.success_address not in self.browser.current_url:
                logger.info('登陆中')
                if count % 30 == 0:
                    try:
                        self.qr_process(username)
                    except Exception as e:
                        logger.error(e)
                else:
                    time.sleep(10)
                count += 1
            return cookie

    def qr_process(self, username):
        try:
            # 点击刷新按钮
            self.browser.execute_script(self.refrash_loc)
        except Exception as e:
            logger.info(e)
        time.sleep(1)
        img_src = self.get_img_src()
        files = {'file': (img_src.split('/')[-1], requests.get(img_src).content)}
        sdata = {'spiderServerName': 'spider-10001', 'msg': username}
        response = requests.post(self.server_address, data=sdata, files=files)
        logger.info(response.status_code)

    def get_img_src(self):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="J_QRCodeImg"]/img'))).get_attribute('src')


if __name__ == '__main__':
    taobaoCookiesGenerator().new_cookies(username='周一')
