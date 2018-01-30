import re


class BookscraperPipeline(object):
    file = None

    def open_spider(self, spider):
        self.file = open(spider.name + "_urls.txt", "w")

    def process_item(self, item, spider):
        if item.get("url"):
            url = re.sub(r'^h?t?t?p?s?:?/?/?w?w?w?\.?', "", item.get("url"))
            self.file.write(url + "\n")

        return item

    def close_spider(self, spider):
        self.file.close()
