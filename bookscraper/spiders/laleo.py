import scrapy


class LaleoSpider(scrapy.Spider):
    name = "laleo.com"

    def start_requests(self):
        urls = [
            'https://www.laleo.com/libros-c-127.html'
        ]

        self.listing_headers={
            "Host": "www.laleo.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        for url in urls:
            page = url.split("127")[1]
            new_url = url.split("127")[0] + "_" + "36" + str(int(page) + 1)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        page = response.url.split("127")[-1]

        for a_tags in response.selector.xpath('//a[@class="product_img_link"]/@href'):
            url = a_tags.extract()
            data = {
                "url": url
            }

            yield data

        meta = {
            "dont_redirect": True
        }
        new_url = response.url.split("&p=")[0] + "&p=" + str(int(page) + 1)
        yield scrapy.Request(url=new_url, callback=self.parse,
                             headers=self.listing_headers, meta=meta)
