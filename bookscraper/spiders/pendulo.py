import re
import scrapy
import pkgutil


class ElPenduloSpider(scrapy.Spider):
    name = "pendulo.com"

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/isbn.txt")
        isbn_list = binary_string.decode("utf-8").split("\n")

        for isbn in isbn_list:
            url = "https://pendulo.com/libreria/" + isbn
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):
        no_product = response.selector.xpath('//div[@style="display:block;"]/*[@id="productoPR_sinProducto"]')
        if no_product:
            return

        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath('//div/h1[@itemprop="name"]/text()').extract_first()),
            "content": self.clean_text(response.selector.xpath('//div[@id="productoPR_descripcion"]/text()').extract_first()),
            "author": self.clean_text(response.selector.xpath('//div/h2[@id="productoPR_autor"]/text()').extract_first()),
            "editorial": self.clean_text(response.selector.xpath('//dl/dd/a[@itemprop="publisher"]/text()').extract_first()),
            "price": self.clean_price(response.selector.xpath('//div/p/span[@itemprop="price"]/text()').extract_first()),
            "ISBN": self.clean_price(response.selector.xpath('//dd[@itemprop="ISBN"]/text()').extract_first())
        }

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