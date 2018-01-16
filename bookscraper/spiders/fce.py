import pkgutil

import scrapy

from .parsers import parse_details_fce


class FondodeCulturaEconomica(scrapy.Spider):
    name = 'fondodeculturaeconomica.com'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.listing_headers = {
            "Host": "www.fondodeculturaeconomica.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/FCE_title.txt")
        title_list = binary_string.decode("utf-8").split("\n")

        title_set = set()
        for title in title_list:
            if len(title) >= 5:
                title_set.add(title)

        for title in title_set:
            url = "https://elfondoenlinea.com/Busqueda.aspx?tit=on&buscar=" + title
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        books_found = 0

        url = response.selector.xpath('//div[@class="row"]//div/a/@href').extract_first()
        if url:
            books_found += 1
            yield scrapy.Request(url="https://elfondoenlinea.com/" + url,
                                 callback=parse_details_fce,
                                 headers=self.listing_headers,
                                 meta=response.meta
                                 )

        if books_found == 0:
            return
