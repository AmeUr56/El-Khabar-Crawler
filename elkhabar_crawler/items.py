# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ElkhabarCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    number_readers = scrapy.Field()
    content = scrapy.Field()
    