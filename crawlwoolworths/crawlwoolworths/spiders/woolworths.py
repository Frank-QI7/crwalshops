# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from crawlwoolworths.items import *
import re
from lxml import etree




class WoolworthsSpider(scrapy.Spider):
    name = 'woolworths'
    pattern = re.compile('[0-9.]+')
    base_url = 'https://www.woolworths.com.au'
    allowed_domains = ['www.woolworths.com.au']
    enable_crawl = ['https://www.woolworths.com.au/shop/browse/fruit-veg?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/pantry?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/drinks?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/liquor?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/baby?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/health-beauty?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/household?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/lunch-box?pageNumber=1',
                    'https://www.woolworths.com.au/Shop/Browse/meat-seafood-deli?pageNumber=1',
                    'https://www.woolworths.com.au/Shop/Browse/bakery?pageNumber=1',
                    'https://www.woolworths.com.au/Shop/Browse/freezer?pageNumber=1',
                    'https://www.woolworths.com.au/Shop/Browse/pet?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/specials/half-price?pageNumber=1',
                    'https://www.woolworths.com.au/shop/browse/specials/prices-dropped?pageNumber=1',
                    ]

    def start_requests(self):
        for url in self.enable_crawl:
            yield scrapy.Request(url=url,callback=self.parse_product)


    def parse_product(self, response):
        selector = pq(response.text)
        products1 = selector('.tile-container.tile-product').items()
        for product in products1:
            item = woolworthsItem()
            name = product('.shelfProductTile-descriptionLink').text().strip()
            image = product('.shelfProductTile-image').attr('src')
            price1 = []
            price1.append(product('.price-dollars').text())
            price1.append(product('.price-cents').text())
            price = '.'.join(price1)
            item['name'] = name
            item['image'] = image
            item['price1'] = price
            item['price2'] = price
            item['location'] = 'WoolWorths'
            yield item

        products2 = selector('.tile-container.tile-bundle').items()
        if products2:
            for product in products2:
                name = product('.shelfBundleTile-title').text().strip()
                variants = product('.shelfBundleTile-item').items()
                for variant in variants:
                    item = woolworthsItem()
                    name1 = name + variant('.shelfProductVariant-variant').text().strip()
                    image = variant('.shelfProductVariant-image').attr('src')
                    try:
                        price = self.pattern.findall(variant('.shelfProductVariant-price').text().strip())[0]
                    except:
                        price = ''
                    item['name'] = name1
                    item['image'] = image
                    item['price1'] = price
                    item['price2'] = price
                    item['location'] = 'WoolWorths'
                    yield item

        next_page = selector('.paging-next._pagingNext').attr('href')
        next_url = self.base_url + next_page
        yield scrapy.Request(url=next_url,callback=self.parse_product)

