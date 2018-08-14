# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChemistItem(scrapy.Item):
    name = scrapy.Field()
    price1 = scrapy.Field()
    price2 = scrapy.Field()
    image = scrapy.Field()
    location = scrapy.Field()