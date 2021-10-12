from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from books_parser import settings
from books_parser.spiders.labirint import LabirintSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)

    process.start()