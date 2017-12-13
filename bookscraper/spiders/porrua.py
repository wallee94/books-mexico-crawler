import pkgutil
import re

import scrapy


class Porrua(scrapy.Spider):
    name = 'porrua.mx'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.listing_headers = {
            "Host": "www.porrua.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/isbn.txt")
        isbn_list = binary_string.decode("utf-8").split("\n")

        for isbn in isbn_list:
            url = "https://www.porrua.mx/libro/GEN:ISBN/autor/titulo/" + isbn
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        isbn = response.url.split("/")[-1]
        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath("//div[@class]/strong[@style][1]/text()").extract_first()),
            "content": "",
            "author": self.clean_text(response.selector.xpath('//div[@class]/p[@style][1]/span/text()').extract_first()),
            "editorial": self.clean_text(response.selector.xpath("//div[@class]/p[@style][2]/span/text()").extract_first()),
            "price": self.clean_price(response.selector.xpath('//div[@class="comprar_precio"]/strong/text()').extract_first()),
            "ISBN": isbn,
        }

        if not data.get("title") or not data.get("price"):
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
            if c.isdigit():
                res += c
        return res
