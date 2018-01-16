import scrapy

from .parsers import parse_details_educal


class EducalSpider(scrapy.Spider):
    name = "educal.com.mx"

    def start_requests(self):
        urls = [
            'https://www.educal.com.mx/seleccion/261-inah/pagina1.html',
            'https://www.educal.com.mx/seleccion/529-inba/pagina1.html',
            'https://www.educal.com.mx/0700-artes/pagina1.html',
            'https://www.educal.com.mx/0500-ciencias-puras/pagina1.html',
            'https://www.educal.com.mx/0300-ciencias-sociales/pagina1.html',
            'https://www.educal.com.mx/0100-filosofia/pagina1.html',
            'https://www.educal.com.mx/0900-historia/pagina1.html',
            'https://www.educal.com.mx/0400-lenguaje/pagina1.html',
            'https://www.educal.com.mx/0800-literatura/pagina1.html',
            'https://www.educal.com.mx/0000-obras-generales/pagina1.html',
            'https://www.educal.com.mx/0200-religion/pagina1.html',
            'https://www.educal.com.mx/0600-tecnologia/pagina1.html',
            'https://www.educal.com.mx/0800-literatura/0890-infantil-y-juvenil/pagina1.html',
            'https://www.educal.com.mx/coleccion/0124-preparatoria-abierta/pagina1.html'
        ]

        self.listing_headers={
            "Host": "www.educal.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)

    def parse(self, response):
        page = response.url.split("pagina")[1].split(".")[0]
        books_found = 0

        for url in response.selector.xpath('//div[@id="item-3d-display"]//div[@class="top"]/a/@href'):
            books_found += 1
            yield scrapy.Request(url=url.extract(), callback=parse_details_educal, headers=self.listing_headers)

        if books_found != 0:
            url = response.url.split("pagina")[0] + "pagina" + str(int(page) + 1) + ".html"
            yield scrapy.Request(url=url, callback=self.parse, headers=self.listing_headers)
