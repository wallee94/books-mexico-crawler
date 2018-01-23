import scrapy


class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    editorial = scrapy.Field()
    price = scrapy.Field()
    ISBN = scrapy.Field()
    image = scrapy.Field()