import scrapy

import re


class SanbornsSpider(scrapy.Spider):
    name = "sanborns.com.mx"

    def start_requests(self):
        urls = [
            'http://www.sanborns.com.mx/_layouts/wpSanborns/GetProductos.aspx?&orden=0' \
            '&filtro=-1&idFamily=' + str(i) + '&page=1' for i in range(50106, 50135)
        ]
        self.details_headers = {
            "Host": "www.sanborns.com.mx",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.details_headers)

    def parse(self, response):
        page = response.url.split("page=")[1]
        books_found = 0

        for div in response.selector.xpath('//div[@class="producto"]'):
            url = div.xpath('./a[1]/@href').extract_first()
            books_found += 1
            data = {
                "url": re.sub("^h?t?t?p?s?:?/?/?w?w?w?", "", url)
            }
            yield data
            if books_found == 12:
                url = response.url.split("page=")[0] + "page=" + str(int(page) + 1)
                yield scrapy.Request(url=url, callback=self.parse, headers=self.details_headers)