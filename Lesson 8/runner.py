from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from instaparser import settings
from instaparser.spiders.insta import InstaSpider
from sys import argv, path

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaSpider, query=argv[1:])

    process.start()
    #print(path)