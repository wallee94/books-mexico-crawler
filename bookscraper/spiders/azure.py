import scrapy
import json


class Azure(scrapy.Spider):
    name = "bing_azure_API"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        query = "site:elfondoenlinea.com"
        self.limit = 23300
        self.base_url = "https://api.cognitive.microsoft.com/bing/v7.0/search?q=" + query + "&count=50&offset="
        self.headers = {
            "Ocp-Apim-Subscription-Key": "0f5e3b448b6c45e0b5ad33f43fcd4fe7"
        }

    def start_requests(self):
        urls = [
            self.base_url + '0'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        start = int(response.url.split("=")[-1])
        items = json.loads(response.body_as_unicode()).get("webPages", {}).get("value", [])
        for item in items:
            yield item

        if start < self.limit - 50:
            yield scrapy.Request(url=self.base_url + str(start + 50), callback=self.parse, headers=self.headers)





