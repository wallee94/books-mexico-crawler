import scrapy


class BuscaLibreSpider(scrapy.Spider):
    name = "buscalibre.com.mx"

    def start_requests(self):
        # get category codes
        url = "https://www.buscalibre.com.mx/libros"
        yield scrapy.Request(url=url, callback=self.parse_category_ids)

    def parse_category_ids(self, response):
        category_selectors = response.selector.xpath('//div[@class="box-list"]/ul/li/a/@href')
        if not category_selectors:
            return

        for category_selector in category_selectors:
            url = category_selector.extract()
            meta = {
                "page": 1,
                "base_url": url,
            }
            yield scrapy.Request(url=url, callback=self.parse_category_books, meta=meta)

    def parse_category_books(self, response):
        if response.selector.xpath('//section[@id="noEncontrado"]'):
            return

        for product_selector in response.selector.xpath('//div[@class="producto "]/a/@href'):
            yield {
                "url": product_selector.extract()
            }

        meta = {
            "page": response.meta.get('page') + 1,
            "base_url": response.meta.get('base_url'),
        }
        try:
            url = meta['base_url'] + "?page=" + str(meta["page"])
            yield scrapy.Request(url=url, callback=self.parse_category_books, meta=meta)
        except ValueError:
            return
