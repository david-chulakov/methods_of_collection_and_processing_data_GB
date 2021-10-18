import scrapy
from scrapy.http import HtmlResponse
from leryaparser.items import LeryaparserItem
from scrapy.loader import ItemLoader

class LeryaSpider(scrapy.Spider):
    name = 'lerya'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_product)


    def parse_product(self, response: HtmlResponse):
        # loader = ItemLoader(item=LeryaparserItem, response=response)
        #
        # loader.add_xpath('name', "//h1[@slot='title']/text()")
        # loader.add_value('link', response.url)
        # loader.add_xpath('price', "//span[@slot='price']/text()")
        # loader.add_xpath("photo", "//picture[@slot='pictures']/source[contains(@data-origin, 'w_2000')]/@srcset")
        #
        # yield loader.load_item()

        link = response.url
        name = response.xpath("//h1[@slot='title']/text()").get()
        price = response.xpath("//span[@slot='price']/text()").get()
        photo = response.xpath("//picture[@slot='pictures']/source[contains(@data-origin, 'w_2000')]/@srcset").getall()
        yield LeryaparserItem(link=link, name=name, price=price, photo=photo)