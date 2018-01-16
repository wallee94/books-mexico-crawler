import re
import scrapy
from .parsers import parse_details_gonvill


class GonvillSpider(scrapy.Spider):
    name = "gonvill.com.mx"

    def start_requests(self):
        urls = ['https://www.gonvill.com.mx/sitemaplibros.xml.php?pag=' + str(i) for i in range(1,21)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.selector.register_namespace('d', 'https://www.google.com/schemas/sitemap/0.84')
        locs = response.selector.xpath("//d:loc/text()")

        self.details_headers = {
            "Host": "www.gonvill.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

        for loc in locs:
            url = loc.extract()
            if "/libro/" in url:
                yield scrapy.Request(url=url, callback=parse_details_gonvill, headers=self.details_headers)
