# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from chemistwarehouse.items import *
import re

class ChemistSpider(scrapy.Spider):
    name = 'chemist'
    number = re.compile('[0-9.]+')
    allowed_domains = ['www.chemistwarehouse.com.au']
    start_urls = ['https://www.chemistwarehouse.com.au/Shop-OnLine/256/Health?size=120',
                  'https://www.chemistwarehouse.com.au/Shop-Online/651/Veterinary?size=120',
                  'https://www.chemistwarehouse.com.au/Shop-Online/260/Medical-Aids?size=120',
                  'https://www.chemistwarehouse.com.au/Shop-Online/259/Personal-Care?size=120',
                  'https://www.chemistwarehouse.com.au/Shop-Online/258/Medicines?size=120',
                  'https://www.chemistwarehouse.com.au/Shop-OnLine/257/Beauty?size=120']

    def start_requests(self):
        for url in self.start_urls:
            #在这里 可以不添加 callback，因为默认就是parse
            yield scrapy.Request(url)

    def parse(self, response):
        pattern = re.compile('page=(\d+)')
        selector = pq(response.text)
        urls = response.url + '&page={page_count}'
        category = selector('#category_title_h1 #category_title_span').text().strip()
        products = selector('#p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem tr td').items()
        for product in products:
            item =ChemistItem()
            img = product('img[class!=product_image_overlay]').attr('src')
            name = product('img[class!=product_image_overlay]').attr('alt').strip()
            price1 = str(product('.Price').text().strip())
            price = self.number.findall(price1)[0]
            item['image'] = img
            item['name'] = name
            item['price1'] = float(price)
            item['price2'] = price
            item['location'] = 'Chemist Warehouse'
            yield item
        try:
            page_count = pattern.findall(str(selector('.last-page').attr('href')))[0]
            for i in range(2, int(page_count) + 1):
                # 在这里 可以不添加 callback，因为默认就是parse，
                # 但是是其他的就必须添加，其实是自己忘记添加了，才发现默认就是parse！！！！！！！！！！！！！！！！！！！！
                yield scrapy.Request(url=urls.format(page_count=i),callback=self.parse_item)
        except:
            page_count = selector('.next-page').attr('href')
            url = 'https://www.chemistwarehouse.com.au' + page_count
            yield scrapy.Request(url,callback=self.parse_item)

    def parse_item(self,response):
        selector = pq(response.text)
        urls = response.url + '&page={page_count}'
        category = selector('#category_title_h1 #category_title_span').text().strip()
        products = selector('#p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem tr td').items()
        for product in products:
            item = ChemistItem()
            img = product('img[class!=product_image_overlay]').attr('src')
            name = product('img[class!=product_image_overlay]').attr('alt').strip()
            price1 = str(product('.Price').text().strip())
            price = self.number.findall(price1)[0]
            item['image'] = img
            item['name'] = name
            item['price1'] = float(price)
            item['price2'] = price
            item['location'] = 'Chemist Warehouse'
            yield item
