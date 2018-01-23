# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookscraperPipeline(object):
    file = None

    def open_spider(self, spider):
        self.file = open(spider.name + "_urls.txt", "w")

    def process_item(self, item, spider):
        if item.get("url"):
            self.file.write(item.get("url") + "\n")

        return item

    def close_spider(self, spider):
        self.file.close()
