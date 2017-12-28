import pkgutil
import re

import scrapy


class Porrua(scrapy.Spider):
    name = 'bookfinder.com'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.listing_headers = {
            "Host": "www.bookfinder.com",
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
            url = "https://www.bookfinder.com/search/?lang=en&new_used=*&destination=mx&currency=MXN&binding=*" \
                  "&mode=advanced&st=sr&ac=qr&keywords=" + isbn
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath('//strong/span[@itemprop="name"]/text()').extract_first()),
            "image": response.selector.xpath('//div/img[@itemprop="image"]/@src').extract_first(),
            "author": self.clean_text(response.selector.xpath('//strong/span[@itemprop="author"]/text()').extract_first()),
            "publisher": self.clean_text(response.selector.xpath('//span[@itemprop="publisher"]/text()').extract_first()),
            "ISBN_10": self.clean_isbn(response.selector.xpath('//div/h1[@style]/span[@itemprop="isbn"]/text()').extract_first()),
            "ISBN_13": self.clean_isbn(response.selector.xpath('//div/h1[@style]/text()').extract_first()),
        }

        if not data.get("title"):
            return

        yield data

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = re.sub("[\n\t]+", "", text)
        text = re.sub("\s+", " ", text)
        return text

    def clean_isbn(self, text):
        if not isinstance(text, str):
            return ""
        return re.sub(r"[^\d]", "", text)

    def clean_price(self, price):
        if not isinstance(price, str):
            return "-1"
        res = ""
        for c in price:
            if c.isdigit():
                res += c
        return res
