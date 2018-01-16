import json

import scrapy

from .parsers import parse_details_gandhi


class GandhiSpider(scrapy.Spider):
    name = "gandhi.com.mx"

    def start_requests(self):
        urls = [
            'http://www.gandhi.com.mx/libros/ficcion?p=1',
            'http://www.gandhi.com.mx/libros/no-ficcion?p=1',
        ]
        self.listing_headers={
            "Host": "www.gandhi.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://www.gandhi.com.mx/libros/ficcion",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            'content-type': 'application/x-www-form-urlencoded'
        }
        self.details_headers={
            "Host": "www.gandhi.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://www.gandhi.com.mx/libros/ficcion",
            "X-Requested-With": "XMLHttpRequest"
        }
        data={
            "isJsonP": "1"
        }
        for url in urls:
            yield scrapy.Request(url=url, body=json.dumps(data), callback=self.parse, method="POST", headers=self.listing_headers)

    def parse(self, response):
        page= response.url.split("=")[1]
        books_found = 0

        for li in response.selector.css("li.item"):
            url= li.xpath("./a/@href").extract_first()
            books_found += 1
            yield scrapy.Request(url=url, callback=parse_details_gandhi, headers=self.details_headers)

        # find new url
        form_data = {
            "isJsonP": "1"
        }
        if books_found == 20:
            url= response.url.split("=")[0] + "=" + str(int(page) + 1)
            yield scrapy.Request(url=url, body=json.dumps(form_data), callback=self.parse, method="POST", headers=self.listing_headers)
