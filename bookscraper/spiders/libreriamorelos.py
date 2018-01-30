import scrapy

import re

class LibreriaMorelosSpider(scrapy.Spider):
    name = "libreriamorelos.mx"

    def start_requests(self):
        urls = [
            'https://libreriamorelos.mx/' + str(i) + '/titulo' for i in range(29890,88200)
        ]

        self.details_headers = {
            "Host": "libreriamorelos.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.details_headers)

    def parse(self, response):
        if response.selector.xpath('//h1[@class="product-title"]'):
            url = response.url.strip()
            if url:
                url = url.replace("http:", "https:")
                data = {
                    "url": re.sub("^h?t?t?p?s?:?/?/?w?w?w?\.?", "", url)
                }
                yield data