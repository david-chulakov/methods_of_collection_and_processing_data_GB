# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import os
from urllib.parse import urlparse


class LeryaparserPipeline:

    def process_item(self, item, spider):
        print()
        return item


class LeryaImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        return 'full/' + item['name'] + "/" + os.path.basename(urlparse(request.url).path)

    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)


    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item