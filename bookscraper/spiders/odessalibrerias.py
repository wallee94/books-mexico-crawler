import scrapy


class OdessaSpider(scrapy.Spider):
    name = "odessalibrerias.com.mx"

    def start_requests(self):
        urls = [
            'https://odessalibrerias.com.mx/index.php?id_category=47&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=45&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=27&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=42&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=41&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=24&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=54&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=14&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=33&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=13&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=31&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=28&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=30&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=15&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=18&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=21&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=40&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=46&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=17&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=23&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=34&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=25&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=16&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=52&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=12&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=37&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=22&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=51&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=29&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=38&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=48&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=50&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=44&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=43&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=35&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=53&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=49&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=36&controller=category&p=1',
            'https://odessalibrerias.com.mx/index.php?id_category=39&controller=category&p=1'
        ]
        self.listing_headers={
            "Host": "odessalibrerias.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://odessalibrerias.com.mx/index.php?id_category=45&controller=category",
            "Connection": "keep-alive",
            'content-type': 'application/x-www-form-urlencoded'
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        page = response.url.split("=")[-1]

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
