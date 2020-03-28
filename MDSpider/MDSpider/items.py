# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_href = scrapy.Field()
    product_price = scrapy.Field()
    product_detail = scrapy.Field()
    # 产品型号
    product_model = scrapy.Field()
    # 数据来源
    source = scrapy.Field()
    # 爬取时间
    ProgramStarttime = scrapy.Field()
    # 品牌
    product_brand = scrapy.Field()
    nowTime = scrapy.Field()
