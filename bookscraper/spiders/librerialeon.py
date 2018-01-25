import scrapy


class LibreriaLeonSpider(scrapy.Spider):
    name = "librerialeon.com.mx"

    def start_requests(self):
        urls = [
            'http://www.librerialeon.com.mx/sitemaplibros.xml.php?pag=' + str(i) for i in range(1,18)
        ]

        self.details_headers = {
            "Host": "www.librerialeon.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.details_headers)

    def parse(self, response):
        response.selector.register_namespace('d', 'http://www.google.com/schemas/sitemap/0.84')
        locs = response.selector.xpath("//d:loc/text()")

        for loc in locs:
            url = loc.extract()
            if "libro" in url:
                url = url.replace("http:", "https:")
                data = {
                    "url": url
                }
                yield data