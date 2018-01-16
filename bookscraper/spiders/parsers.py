import re


def parse_details_alfaomega(response):
    data = {
        "url": response.url.strip(),
        "title": clean_text(response.selector.xpath("//h1/text()").extract_first()),
        "content": clean_text(response.selector.xpath('//div[@class="std"]/child::p/text()').extract_first()),
        "author": clean_text(
            response.selector.xpath('//table[@class="data-table"]//tbody/tr[1]/td/text()').extract_first()),
        "price": clean_price(
            response.selector.xpath('//div[@class="product-info"]/span[2]/text()').extract_first()),
        "editorial": clean_text(
            response.selector.xpath('//table[@class="data-table"]//tbody/tr[2]/td/text()').extract_first()),
        "ISBN": clean_isbn(
            response.selector.xpath('//table[@class="data-table"]//tbody/tr[4]/td/text()').extract_first()),
        "image_url": response.selector.xpath('//div[@id="image"]/img/@src').extract_first(),
    }

    if not data.get("title") or not data.get("price") or not data.get("ISBN"):
        return

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data


def parse_details_casadelibro(response):
    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath("//h1/text()").extract_first()),
        "content": "",
        "author": clean_text(response.selector.xpath('//*[@id="product_man"]/a/span/text()').extract_first()),
        "editorial": "",
        "price": clean_price(response.selector.xpath('//*[@itemprop="price"]/text()').extract_first()),
        "ISBN": clean_price(response.selector.xpath('//*[@itemprop="sku"]/text()').extract_first())
    }

    if data["price"] == -1 or data["ISBN"] == -1:
        return

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data


def parse_details_educal(response):
    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath('//div[@class="col-md-6 info-panel"]/span[@class="title"]/text()').extract_first()),
        "content": clean_text(response.selector.xpath('//div[@class="sinopsis-text"]/text()').extract_first()),
        "author": clean_text(response.selector.xpath('//span/a/text()').extract_first()),
        "price": clean_price(response.selector.xpath('//div[@class="col-md-6 info-panel"]//div[@class="price"]/text()').extract_first()),
        "ISBN": clean_price(response.selector.xpath('//td/span[text()="ISBN"]/parent::td/text()').extract_first())
    }

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data
    
    
def parse_details_fce(response):
    prices = response.selector.xpath('//ul[@class="nav fce-buttons-buy-container"]/li/ul[@class="nav fce-det-buy-container"]/li[2]/text()')
    isbns = response.selector.xpath('//ul[@class="nav fce-buttons-buy-container"]/div/div/text()')
    isbns = isbns[:len(prices)]  # to drop isbns from electronic books

    for price, isbn in zip(prices, isbns):
        print(price.extract(), isbn.extract())

        data = {
            "url": clean_url(response.url.strip()),
            "title": clean_text(response.selector.xpath('//li/span[@class="text-titulo"]/text()').extract_first()),
            "content": clean_text(response.selector.xpath('//div/div[@class="col-md-12"][1]/text()').extract_first()),
            "author": clean_text(response.selector.xpath('//li/span[@class="text-autor"][1]/text()').extract_first()),
            "price": clean_price(price.extract()),
            "editorial": clean_text(response.selector.xpath('//li/span[@class="text-editorial"]/text()').extract_first()),
            "ISBN": clean_isbn(isbn.extract()),
        }

        if not data.get("title") or not data.get("price") or not data.get("ISBN"):
            return

        old_price = response.meta.get("price")
        try:
            new_price = float(data["price"])
        except ValueError:
            continue

        if not old_price or new_price != old_price:
            yield data


def parse_details_gandhi(response):
    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath("//form//h1/text()").extract_first()),
        "content": clean_text(response.selector.xpath("//form//dd/div/div/text()").extract_first()),
        "author": clean_text(response.selector.xpath("//form//h2[1]/a/text()").extract_first()),
        "editorial": clean_text(response.selector.xpath("//form//h2[2]/a/text()").extract_first()),
        "price": clean_price(response.selector.xpath('//span[@class="price"]/text()').extract_first()),
        "ISBN": clean_price(response.selector.xpath("//dd//tbody/tr[6]/td").extract_first())
    }

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data
    
    
def parse_details_gonvill(response):
    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath("//div/dl/h1/text()").extract_first()),
        "content": clean_text(response.selector.xpath('//div/p[@itemprop="description"]/text()').extract_first()),
        "author": clean_text(response.selector.xpath("//div/dl/p/a/text()").extract_first()),
        "editorial": clean_text(response.selector.xpath('//div/dl/dd/a[@itemprop="publisher"]/text()').extract_first()),
        "price": clean_price(response.selector.xpath('//div/span[@itemprop="price"]/text()').extract_first()),
        "ISBN": clean_price(response.selector.xpath('//div//dl/dd[@itemprop="isbn"]/text()').extract_first())
    }

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data
    
    
def parse_details_pendulo(response):
    no_product = response.selector.xpath('//div[@style="display:block;"]/*[@id="productoPR_sinProducto"]')
    if no_product:
        return

    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath('//div/h1[@itemprop="name"]/text()').extract_first()),
        "content": clean_text(response.selector.xpath('//div[@id="productoPR_descripcion"]/text()').extract_first()),
        "author": clean_text(response.selector.xpath('//div/h2[@id="productoPR_autor"]/a/text()').extract_first()),
        "editorial": clean_text(response.selector.xpath('//dl/dd/a[@itemprop="publisher"]/text()').extract_first()),
        "price": clean_price(response.selector.xpath('//div/p/span[@itemprop="price"]/text()').extract_first()),
        "ISBN": clean_price(response.selector.xpath('//dd[@itemprop="ISBN"]/text()').extract_first())
    }

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data
    
    
def parse_details_porrua(response):
    isbn = response.url.split("/")[-1]
    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath("//div[@class]/strong[@style][1]/text()").extract_first()),
        "content": "",
        "author": clean_text(response.selector.xpath('//div[@class]/p[@style][1]/span/text()').extract_first()),
        "editorial": clean_text(response.selector.xpath("//div[@class]/p[@style][2]/span/text()").extract_first()),
        "price": clean_price(response.selector.xpath('//div[@class="comprar_precio"]/strong/text()').extract_first()),
        "ISBN": isbn,
    }

    if not data.get("title") or not data.get("price"):
        return

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data
    
    
def parse_details_sotano(response):
    data = {
        "url": response.url,
        "title": clean_text(response.selector.xpath("//div/div/h1/text()").extract_first()),
        "content": clean_text(response.selector.xpath("//div/div/section/div[1]/p/text()").extract_first()),
        "author": clean_text(response.selector.xpath('//div[@class="descripcion-libro DER"]/a/text()').extract_first()),
        "editorial": clean_text(response.selector.xpath("//div/div/span/a/text()").extract_first()),
        "price": clean_price(response.selector.xpath('//div/div/div/p/span[2]/text()').extract_first()),
        "ISBN": response.meta.get("isbn")
    }

    if not data.get("title") or not data.get("price"):
        return

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub("\t+", "", text)
    text = re.sub("\n+", "", text)
    text = re.sub("\r+", "", text)
    text = re.sub("\\s{2,}", " ", text)
    return text


def clean_isbn(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r"[^\d]", "", text)


def clean_price(price):
    if not isinstance(price, str):
        return "-1"
    res = ""
    for c in price:
        if c.isdigit() or c == ".":
            res += c
    return res


def clean_url(url):
    return re.sub(r'[%20]+$', "", url)
