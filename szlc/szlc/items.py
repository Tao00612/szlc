# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SzlcItem(scrapy.Item):
    # define the fields for your item here like:
    b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_cate_url = scrapy.Field()
    model = scrapy.Field()
    brand = scrapy.Field()
    brand_url = scrapy.Field()
    parameter = scrapy.Field()
    specifications = scrapy.Field()
    goods_is = scrapy.Field()
    recentlySalesCount = scrapy.Field()
    data = scrapy.Field()

