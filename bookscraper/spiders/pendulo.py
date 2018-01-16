import pkgutil

import scrapy

from .parsers import parse_details_pendulo


class ElPenduloSpider(scrapy.Spider):
    name = "pendulo.com"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.details_headers = {
            "Host": "pendulo.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/isbn.txt")
        isbn_list = binary_string.decode("utf-8").split("\n")

        for isbn in isbn_list:
            url = "https://pendulo.com/libreria/" + isbn
            yield scrapy.Request(url=url, callback=parse_details_pendulo, headers=self.details_headers)
