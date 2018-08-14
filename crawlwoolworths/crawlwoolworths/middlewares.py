import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.chrome.options import Options
from scrapy import signals
from scrapy.http import HtmlResponse
from logging import getLogger
import time
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

class SeleniumMiddleware():
    def __init__(self,timeout=None, service_args=[]):
        LOGGER.setLevel(logging.WARNING)
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用PhantomJS抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        try:
            self.browser.get(request.url)
            # back = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.browseLeftPanel-headingLink')))
            # back.click()
            # show_all = self.wait.until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, '.categoriesNavigation-linkShowall')))
            # show_all.click()
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.shelfProductTile-descriptionLink')))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.shelfProductTile-image')))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.price-dollars')))
            js = "var q=document.documentElement.scrollTop=100000"
            self.browser.execute_script(js)
            time.sleep(1)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))