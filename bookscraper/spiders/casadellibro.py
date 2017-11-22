import pkgutil
import re

import scrapy


class CasaDelLibroSpider(scrapy.Spider):
    name = "casadelibro.com.mx"
    download_delay = 8

    crawlera_enabled = True
    crawlera_apikey = 'ed62d130ee8a4973a72ef0a1b81b3a29'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        binary_string = pkgutil.get_data("bookscraper", "resources/casadelibro_requests_done.txt")
        self.requests_done = binary_string.decode("utf-8").split("\n")

        self.details_headers = {
            "Host": "casadelibro.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Connection": "keep-alive"
        }

    def start_requests(self):
        urls = ['http://casadelibro.com.mx/1_es_' + str(i) + '_sitemap.xml' for i in range(5)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        locs = response.selector.xpath("//d:loc/text()")

        for loc in locs:
            url = loc.extract()
            if ".pdf" not in url and url not in self.requests_done:
                yield scrapy.Request(url=url, headers=self.details_headers, cookies={}, callback=self.parse_details)

    def parse_details(self, response):
        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath("//h1/text()").extract_first()),
            "content": "",
            "author": self.clean_text(response.selector.xpath('//*[@id="product_man"]/a/span/text()').extract_first()),
            "editorial": "",
            "price": self.clean_price(response.selector.xpath('//*[@itemprop="price"]/text()').extract_first()),
            "ISBN": self.clean_price(response.selector.xpath('//*[@itemprop="sku"]/text()').extract_first())
        }

        if data["price"] == -1 or data["ISBN"] == -1:
            return

        yield data

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = re.sub("[\n\t]+", "", text)
        text = re.sub("\s+", " ", text)
        return text

    def clean_price(self, price):
        if not isinstance(price, str):
            return "-1"
        res = ""
        for c in price:
            if c.isdigit() or c == ".":
                res += c
        return res