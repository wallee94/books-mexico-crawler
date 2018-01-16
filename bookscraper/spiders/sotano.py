import pkgutil

import scrapy

from .parsers import parse_details_sotano


class ElSotano(scrapy.Spider):
    name = 'elsotano.com'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.listing_headers={
            "Host": "www.elsotano.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/isbn.txt")
        isbn_list = binary_string.decode("utf-8").split("\n")

        for isbn in isbn_list:
            url = "https://www.elsotano.com/busqueda.php?q=" + isbn
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers, meta={"isbn":isbn})

    def parse(self, response):
        books_found = 0

        for li in response.selector.css("li.grid"):
            url = li.xpath("./figure/a/@href").extract_first()
            if url:
                books_found += 1
                yield scrapy.Request(url="https://www.elsotano.com/" + url,
                                     callback=parse_details_sotano,
                                     headers=self.listing_headers,
                                     meta=response.meta
                                     )

        if books_found == 0:
            return