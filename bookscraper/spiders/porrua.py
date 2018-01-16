import pkgutil

import scrapy

from .parsers import parse_details_porrua


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
            yield scrapy.Request(url=url, callback=parse_details_porrua, headers=self.listing_headers)

