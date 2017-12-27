import pkgutil
import re

import scrapy


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
                                 callback=self.parse_details,
                                 headers=self.listing_headers,
                                 meta=response.meta
                                 )

        if books_found == 0:
            return

    def parse_details(self, response):
        prices = response.selector.xpath('//ul[@class="nav fce-buttons-buy-container"]/li/ul/li[2]/text()')
        isbns = response.selector.xpath('//ul[@class="nav fce-buttons-buy-container"]/div/div/text()')

        for price, isbn in zip(prices, isbns):
            data={
                "url": response.url.strip(),
                "title": self.clean_text(response.selector.xpath('//li/span[@class="text-titulo"]/text()').extract_first()),
                "content": self.clean_text(response.selector.xpath('//div/div[@class="col-md-12"][1]/text()').extract_first()),
                "author": self.clean_text(response.selector.xpath('//li/span[@class="text-autor"][1]/text()').extract_first()),
                "price": self.clean_price(price.extract_first()),
                "editorial": self.clean_text(response.selector.xpath('//li/span[@class="text-editorial"]/text()').extract_first()),
                "ISBN": self.clean_isbn(isbn.extract_first()),
            }

            if not data.get("title") or not data.get("price") or not data.get("ISBN"):
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
            if c.isdigit() or c == ".":
                res += c
        return res
