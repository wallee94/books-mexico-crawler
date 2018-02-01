import scrapy


class EdimsaSpider(scrapy.Spider):
    name = "edimsa.com.mx"

    def start_requests(self):
        urls = [
            'https://www.edimsa.com.mx/categoria/' + str(i) for i in range(1,250)
        ]

        self.details_headers = {
            "Host": "www.edimsa.com.mx",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.details_headers)

    def parse(self, response):
        if response.selector.xpath('//div[@id="books-container"]'):
            url = response.selector.xpath('//div[@id="books-container"]/div[@class="book-listing"]/div/a/@href').extract_first()
            if url:
                yield {
                    "url": "https://www.edimsa.com.mx" + url
                }