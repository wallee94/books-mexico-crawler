import json
import pkgutil

import scrapy


class GandhiDiscoverySpider(scrapy.Spider):
    name = "busqueda.gandhi.com.mx"

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/isbn.txt")
        isbn_list = binary_string.decode("utf-8").split("\n")

        for isbn in isbn_list:
            if len(isbn) == 13:
                isbn = isbn.strip()
                url = "http://busqueda.gandhi.com.mx/busca?ajaxSearch=1&q=" + isbn
                yield scrapy.Request(url=url, callback=self.parse, meta={"ISBN": isbn})

    def parse(self, response):
        response_obj = json.loads(response.body_as_unicode())
        products = response_obj["productsInfo"].get("products")
        if products:
            product = products[0]

            if not product.get("skus"):
                return

            skus = product.get("skus")[0]
            data = {
                "url": product.get("productUrl"),
                "title": product.get("name"),
                "content": "",
                "author": product.get("authorName"),
                "editorial": "",
                "price": product.get("discountedPriceRaw"),
                "ISBN": skus.get("id", "")
            }

            if data["ISBN"] != response.meta.get("ISBN") \
                    or not data["url"] \
                    or not data["title"] \
                    or not data["price"]:
                return

            data["url"] = "https:" + data["url"]
            yield data
