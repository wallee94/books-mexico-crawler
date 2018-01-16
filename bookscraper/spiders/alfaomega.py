import scrapy

from .parsers import parse_details_alfaomega


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
        start_urls = [
            "https://www.alfaomega.com.mx/default/catalogo/escolar-2.html?limit=48",
            "https://www.alfaomega.com.mx/default/catalogo/profesional.html?limit=48",
            "https://www.alfaomega.com.mx/default/catalogo/interes-general.html?limit=48",
            "https://www.alfaomega.com.mx/default/catalogo/servicios-ao.html?limit=48"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        urls = response.selector.xpath("//div[@class='product-image']/div/div/div/div[1]/a/@href")
        next_page = response.selector.xpath("//a[@class='next i-next']/@href").extract_first()
        for url_selector in urls:
            yield scrapy.Request(url=url_selector.extract(), callback=parse_details_alfaomega, headers=self.headers)

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)
