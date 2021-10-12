# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksParserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
