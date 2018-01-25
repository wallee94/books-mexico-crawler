import scrapy
import json


class LaleoSpider(scrapy.Spider):
    name = "laleo.com"

    def start_requests(self):
        # get category codes
        url = "https://www.laleo.com/libros-c-127.html"
        yield scrapy.Request(url=url, callback=self.parse_category_ids)

    def parse_category_ids(self, response):
        for category_id in response.selector.re(r"127_(\d+)"):
            body = {
                "container": "listing",
                "page": "0",
                "limit": "20",
                "type": "category",
                "group": category_id,
                "filter": "undefined",
                "sort": "undefined",
                "keywords": "",
            }
            url = "https://www.laleo.com/load_more_products.php"
            meta = {
                "page": 0,
                "category_id": category_id,
            }
            yield scrapy.FormRequest(url=url, formdata=body, callback=self.parse_category_books, meta=meta)

    def parse_category_books(self, response):
        response_obj = json.loads(response.body_as_unicode())
        rq_status = response_obj.get("rq_status")
        if not rq_status or rq_status == "empty":
            return

        products = response_obj.get("products")
        if not products:
            return

        for product in products.get("listing", []):
            yield {
                "url": product.get("link")
            }

        try:
            actual_page = int(response.meta.get("page"))
        except ValueError:
            return
        category_id = response.meta.get("category_id")
        body = {
            "container": "listing",
            "page": str(actual_page + 1),
            "limit": "20",
            "type": "category",
            "group": category_id,
            "filter": "undefined",
            "sort": "undefined",
            "keywords": "",
        }
        meta = {
            "page": body["page"],
            "category_id": category_id,
        }
        url = "https://www.laleo.com/load_more_products.php"
        yield scrapy.FormRequest(url=url, formdata=body, callback=self.parse_category_books, meta=meta)
