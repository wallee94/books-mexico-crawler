import pkgutil
import re

import scrapy


class ElPenduloSpider(scrapy.Spider):
    name = "quelibroleo.com"

    def start_requests(self):
        binary_string = pkgutil.get_data("bookscraper", "resources/quelibroleo_sitemap.txt")
        urls = binary_string.decode("utf-8").split("\n")

        details_headers = {
            "Host": "www.quelibroleo.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept-Encoding": "gzip, deflate, sdch",
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details, headers=details_headers)

    def parse_details(self, response):
        no_product = response.selector.xpath('//div[@style="display:block;"]/*[@id="productoPR_sinProducto"]')
        if no_product:
            return

        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath('//*[@class="libro_info"]/div/h3/text()').extract_first()),
            "content": self.clean_text(response.selector.xpath('//*[@class="content_libro"]/p/text()').extract_first()),
            "author": self.clean_text(response.selector.xpath('//*[@class="libro_info"]//small/a/text()').extract_first()),
        }

        lis = response.selector.xpath('//ul[@class="list"]/li')
        for li in lis:
            label = li.xpath("./span/text()").extract_first().lower()
            if label == "editorial":
                data["editorial"] = self.clean_text(li.xpath("./a/text()").extract_first())
            elif label == "isbn":
                data["ISBN"] = self.clean_text(li.xpath("./text()").extract_first())

        if not data.get("title") or not data.get("ISBN"):
            return

        yield data

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = re.sub("[\n\t]+", "", text)
        text = re.sub("\s+", " ", text)
        return text
