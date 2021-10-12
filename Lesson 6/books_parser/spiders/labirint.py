import scrapy
from scrapy.http import HtmlResponse
from books_parser.items import BooksParserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = [f'https://www.labirint.ru/books/?page={i}' for i in range(1, 18)]
    book_id = 1

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='product-title-link']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath('//h1/text()').get()
        try:
            authors, title = title.split(":")
        except Exception:
            authors = None
            title = title
        try:
            old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        except Exception:
            try:
                old_price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
            except Exception:
                old_price = None
        try:
            new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        except Exception:
            new_price = None
        rating = response.xpath("//div[@id='rate']/text()").get()
        link = 'https://www.labirint.ru/books/' + response.xpath("//div[@class='articul']/text()").get()
        link = link.replace("ID товара: ", "")
        id = response.xpath("//div[@class='articul']/text()").get()
        id = id.replace("ID товара: ", "")
        item = BooksParserItem(_id=id, title=title, authors=authors, old_price=old_price, new_price=new_price, link=link, rating=rating)
        yield item
