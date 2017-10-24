import scrapy
import json
import re


class SotanoSpider(scrapy.Spider):
    name = "elsotano.com"

    def start_requests(self):
        urls = [
            'https://www.elsotano.com/libros_tema-literatura-405?page=0',
            'https://www.elsotano.com/libros_tema-historia-401?page=0',
        ]
        self.listing_headers={
            "Host": "www.elsotano.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        page= response.url.split("=")[1]
        books_found = 0

        headers = self.listing_headers.copy()
        headers["Referer"] = response.url.split("?")[0]

        for figure in response.selector.css("figure.effect-zoe"):
            url= figure.xpath("a/@href").extract_first()
            books_found += 1
            yield scrapy.Request(url="https://www.elsotano.com/" + url, callback=self.parse_details, headers=headers)

        # find new url
        if books_found == 16:
            url= response.url.split("=")[0] + "=" + str(int(page) + 1)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)


    def parse_details(self, response):
        data={
            "url": response.url,
            "title": self.clean_text(response.selector.xpath("//div/div/h1/text()").extract_first()),
            "content": self.clean_text(response.selector.xpath("//div/div/section/div[1]/p/text()").extract_first()),
            "author": self.clean_text(response.selector.xpath('//div[@class="descripcion-libro DER"]/a/text()').extract_first()),
            "editorial": self.clean_text(response.selector.xpath("//div/div/span/a/text()").extract_first()),
            "price": self.clean_price(response.selector.xpath('//div/div/div/p/span[2]/text()').extract_first()),
            "ISBN": self.clean_price(response.selector.xpath("//div/div/div/div/span[5]/text()").extract_first())
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
            if c.isdigit():
                res += c
        return res
