# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from crawlcoles.items import *
import re
from lxml import etree


class ColesSpider(scrapy.Spider):
    name = 'coles'

    # allowed_domains = ['shop.coles.com.au']

    def start_requests(self):
        yield scrapy.Request(url='https://shop.coles.com.au/a/a-national/everything/browse', meta={'getpage': True},callback=self.parse)

    def parse(self, response):
        selector = etree.HTML(response.text)
        urls = selector.xpath("//li[@class='cat-nav-item']/a/@href")
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, meta={'getpage': True},callback=self.parse_product)

    def parse_product(self,response):
        selector = etree.HTML(response.text)
        urls = selector.xpath("//li[@class='cat-nav-item']/a/@href")
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, meta={'getpage': False}, callback=self.parse_page)

    def parse_page(self,response):
        number = re.compile('[0-9.]+')
        pattern = re.compile('pageNumber=(\d)')
        selector = pq(response.text)
        ## 虽然和parse_detail里的内容一样，但是不能直接调用该函数，会导致第一页被过滤掉！！！！！！！！！！！！！！
        base_url = 'https://shop.coles.com.au'
        products = selector('.colrs-animate.tile-animate').items()
        for product in products:
            item = ColesItem()
            name = product('.product-image img').attr('alt')
            if not name:
                continue
            image = base_url + product('.product-image img').attr('src')
            qty = product('.product-qty').text().strip()
            text = product('.product-text').text().strip()
            price1 = str(product('.product-price').text().strip())
            try:
                price = number.findall(price1)[0]
            except:
                price =''

            item['price1'] = price

            if qty != '1':
                price = qty + text + price

            item['image'] = image
            item['name'] = name
            item['price2'] = price
            item['location'] = 'Coles'
            yield item

        page_count = selector('.pagination .page-number a').items()
        if page_count:
            for p in page_count:
                count = p('.number').text()
                url = pattern.sub('pageNumber=' + count, response.url)
                yield scrapy.Request(url=url, meta={'getpage': False}, callback=self.parse_detail)


    def parse_detail(self,response):
        selector = pq(response.text)
        number = re.compile('[0-9.]+')
        base_url = 'https://shop.coles.com.au'
        products = selector('.colrs-animate.tile-animate').items()
        for product in products:
            item = ColesItem()
            name = product('.product-image img').attr('alt')
            if not name:
                continue
            image = base_url + product('.product-image img').attr('src')
            qty = product('.product-qty').text().strip()
            text = product('.product-text').text().strip()
            price1 = str(product('.product-price').text().strip())
            try:
                price = number.findall(price1)[0]
            except:
                price = ''

            item['price1'] = price

            if qty != '1':
                price = qty + text + price

            item['image'] = image
            item['name'] = name
            item['price2'] = price
            item['location'] = 'Coles'
            yield item

