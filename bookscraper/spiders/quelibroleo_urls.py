import scrapy
import json


class QueLibroLeoUrls(scrapy.Spider):
    name = "quelibroleo.com_urls"
    download_delay = 5

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.base_url = "https://www.googleapis.com/customsearch/v1?cx=014231776879756572980:70hevpacd8y&key=AIzaSyAD_pcxkDXpOk4rmw_PpkaaCfA-6bH6qFg&q=libro&num=10&start="

    def start_requests(self):
        urls = [
            self.base_url + '1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        start = int(response.url.split("=")[-1])
        items = json.loads(response.body_as_unicode()).get("items")
        for item in items:
            yield item

        if start < 130000 - 10:
            yield scrapy.Request(url=self.base_url + str(start + 10), callback=self.parse)





