import pkgutil
import re

import scrapy


class Alfaomega(scrapy.Spider):
    name = "alfaomega.com.mx"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

    def start_requests(self):
        url = "https://www.alfaomega.com.mx/default/catalogo.html"
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        urls = response.selector.xpath("//div[@class='product-image']/div/div/div/div[1]/a/@href")
        next_page = response.selector.xpath("//a[@class='next i-next']/@href").extract_first()
        for url_selector in urls:
            yield scrapy.Request(url=url_selector.extract(), callback=self.parse_details, headers=self.headers)

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)

    def parse_details(self, response):
        data = {
            "url": response.url.strip(),
            "title": self.clean_text(response.selector.xpath("//div[@class='product-name']").extract_first()).capitalize(),
            "content": self.clean_text(response.selector.xpath("//div[@class='std']/child::p/text()").extract_first()),
            "author": self.clean_text(response.selector.xpath("//table[@class='data-table']//tbody/tr[1]/td/text()").extract_first()).capitalize(),
            "price": self.clean_price(response.selector.xpath("//div[@class='product-info']/span[2]/text()").extract_first()),
            "editorial": self.clean_text(response.selector.xpath("//table[@class='data-table']//tbody/tr[2]/td/text())").extract_first()).capitalize(),
            "ISBN": self.clean_isbn(response.selector.xpath("//table[@class='data-table']//tbody/tr[4]/td").extract_first()),
        }

        if not data.get("title") or not data.get("price") or not data.get("ISBN"):
            return

        yield data

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = re.sub("\t+", "", text)
        text = re.sub("\n+", "", text)
        text = re.sub("\r+", "", text)
        text = re.sub("\\s{2,}", " ", text)
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

