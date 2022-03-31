# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboKyqzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 源数据
    source_data = scrapy.Field()
    # 表名
    table_name = scrapy.Field()
    pass
