from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leryaparser import settings
from leryaparser.spiders.lerya import LeryaSpider

from sys import argv

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeryaSpider, query=argv[1])

    process.start()
