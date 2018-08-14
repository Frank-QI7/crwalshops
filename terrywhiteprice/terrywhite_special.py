import scrapy
from lxml import etree
from pyquery import PyQuery as pq
from terrywhiteprice.items import *
import re

class TerrywhiteSpider(scrapy.Spider):
    name = 'terrywhite'
    allowed_domains = ['shop.terrywhitechemmart.com.au']
    start_urls = ['https://shop.terrywhitechemmart.com.au/specials/catalogue.html?limit=48']


    def parse(self, response):
        selector = pq(response.text)
        number = re.compile('[0-9.]+')
        pattern = re.compile("[a-zA-Z]+://[^\s']*")
        selector1 = pq(response.text)
        button = str(selector1('.next-btn-new').attr('onclick'))
        producets = selector('.item2').items()
        for product in producets:
            item = TerrywhiteItem()
            img = product('.product-img a img').attr('src')
            #同时选择 两个 class！！！！！
            name = product('.product-list-main.g-product-list-main a').attr('title')
            price = str(product('.prod-price').text().strip())
            item['image'] = img
            item['name'] = name
            try:
                item['price'] = number.findall(price)[0]
            except:
                item['price'] = ''
            item['location'] = 'Terrywhite'
            yield item
        try:
            url = pattern.findall(button)[0]
            yield scrapy.Request(url=url, callback=self.parse)
        except:
            return None
        
