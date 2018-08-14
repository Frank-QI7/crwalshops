# -*- coding: utf-8 -*-
import scrapy
import logging
from lxml import etree
from pyquery import PyQuery as pq
from terrywhiteprice.items import *
import re

class TerrywhiteSpider(scrapy.Spider):
    name = 'terrywhite'
    logger = logging.getLogger(__name__)
    allowed_domains = ['shop.terrywhitechemmart.com.au']
    start_urls = ['https://shop.terrywhitechemmart.com.au']


    def parse(self, response):
        selector = etree.HTML(response.text)
        main_category = selector.xpath('//li[@class="main-li-menu"]/a/@href')
        for url in main_category:
            yield scrapy.Request(url=url, callback=self.parse_maincategory)

    def parse_maincategory(self,response):
        selector= etree.HTML(response.text)
        detail_category = selector.xpath("//div[@class='category-img']/a/@href")
        for url in detail_category:
            yield scrapy.Request(url=url, callback=self.parse_page_index)


    def parse_page_index(self,response):
        self.logger.debug('正在爬取：')
        self.logger.debug(response.url)
        pattern = re.compile("[a-zA-Z]+://[^\s']*")
        number = re.compile('[0-9.]+')
        selector1 = pq(response.text)
        button = str(selector1('.next-btn-new').attr('onclick'))
        selector = pq(response.text)
        # category = selector('title').text()
        products = selector('.item2').items()
        for product in products:
                item = TerrywhiteItem()
                # 下载只是获取的小图片135px，可以吧small_image/135x/  换成image/ 就可以了
                img = product('.product-img a img').attr('src')
                #同时选择 两个 class！！！！！
                name = product('.product-list-main.g-product-list-main a').attr('title')
                price = str(product('.prod-price').text().strip())
                item['image'] = img
                item['name'] = name
                try:
                    item['price1'] = number.findall(price)[0]
                    item['price2'] = number.findall(price)[0]
                except:
                    item['price1'] = ''
                    item['price2'] = ''
                item['location'] = "Terrywhite"
                yield item

        try:
            url = pattern.findall(button)[0]
            yield scrapy.Request(url=url, callback=self.parse_page_index)
        except:
            return None



