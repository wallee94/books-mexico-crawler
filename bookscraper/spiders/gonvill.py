import re

import scrapy


class GonvillSpider(scrapy.Spider):
    name = "gonvill.com.mx"

    def start_requests(self):
        urls = ['https://www.gonvill.com.mx/sitemaplibros.xml.php?pag=' + str(i) for i in range(1,21)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.selector.register_namespace('d', 'https://www.google.com/schemas/sitemap/0.84')
        locs = response.selector.xpath("//d:loc/text()")

        self.details_headers = {
            "Host": "www.gonvill.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

        for loc in locs:
            url = loc.extract()
            if "/libro/" in url:
                yield scrapy.Request(url=url, callback=self.parse_details, headers=self.details_headers)

    def parse_details(self, response):
        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath("//div/dl/h1/text()").extract_first()),
            "content": self.clean_text(response.selector.xpath('//div/p[@itemprop="description"]/text()').extract_first()),
            "author": self.clean_text(response.selector.xpath("//div/dl/p/a/text()").extract_first()),
            "editorial": self.clean_text(response.selector.xpath('//div/dl/dd/a[@itemprop="publisher"]/text()').extract_first()),
            "price": self.clean_price(response.selector.xpath('//div/span[@itemprop="price"]/text()').extract_first()),
            "ISBN": self.clean_price(response.selector.xpath('//div//dl/dd[@itemprop="isbn"]/text()').extract_first())
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