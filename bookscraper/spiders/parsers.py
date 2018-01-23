import re

from bookscraper.items import BookItem


def parse_details_alfaomega(response):
    data = BookItem(
        url=response.url.strip(),
        title=clean_text(response.selector.xpath("//h1/text()").extract_first()),
        content=clean_text(response.selector.xpath('//div[@class="std"]/child::p/text()').extract_first()),
        author=clean_text(response.selector.xpath('//table[@class="data-table"]//tbody/tr[1]/td/text()').extract_first()),
        price=clean_price(response.selector.xpath('//div[@class="product-info"]/span[2]/text()').extract_first()),
        editorial=clean_text(response.selector.xpath('//table[@class="data-table"]//tbody/tr[2]/td/text()').extract_first()),
        ISBN=clean_isbn(response.selector.xpath('//table[@class="data-table"]//tbody/tr[4]/td/text()').extract_first()),
        image=response.selector.xpath('//div[@id="image"]/img/@src').extract_first(),
    )

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
    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath("//h1/text()").extract_first()),
        content="",
        author=clean_text(response.selector.xpath('//*[@id="product_man"]/a/span/text()').extract_first()),
        editorial="",
        price=clean_price(response.selector.xpath('//*[@itemprop="price"]/text()').extract_first()),
        ISBN=clean_price(response.selector.xpath('//*[@itemprop="sku"]/text()').extract_first()),
        image=response.selector.xpath('//span[@id]/img[@id]').extract_first()
    )

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
    div_selectors = response.selector.xpath('//div[@id="item-3d-display"]//*[@class="row-fluid"]/div')
    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath('//div[@class="col-md-6 info-panel"]/span[@class="title"]/text()').extract_first()),
        content=clean_text(response.selector.xpath('//div[@class="sinopsis-text"]/text()').extract_first()),
        author=clean_text(response.selector.xpath('//span/a/text()').extract_first()),
        price=clean_price(response.selector.xpath('//div[@class="col-md-6 info-panel"]//div[@class="price"]/text()').extract_first()),
        ISBN=clean_price(response.selector.xpath('//td/span[text()="ISBN"]/parent::td/text()').extract_first())
    )
    images = div_selectors.re("background-image:url\((.*?)\)")
    default_image = "https://www.educal.com.mx/imagenes_libros/default.gif"

    if images and default_image != images[0]:
        data["image"] = images[0].strip()

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
    isbns = isbns[:len(prices)]  # to drop isbn from electronic books

    for price, isbn in zip(prices, isbns):
        print(price.extract(), isbn.extract())

        data = BookItem(
            url=clean_url(response.url.strip()),
            title=clean_text(response.selector.xpath('//li/span[@class="text-titulo"]/text()').extract_first()),
            content=clean_text(response.selector.xpath('//div/div[@class="col-md-12"][1]/text()').extract_first()),
            author=clean_text(response.selector.xpath('//li/span[@class="text-autor"][1]/text()').extract_first()),
            price=clean_price(price.extract()),
            editorial=clean_text(response.selector.xpath('//li/span[@class="text-editorial"]/text()').extract_first()),
            ISBN=clean_isbn(isbn.extract()),
            image=response.selector.xpath('//img[@class="img-det"]/@src').extract_first()
        )

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
    price_list = response.selector.xpath('//span[@class="price"]/text()')
    if not price_list:
        return

    price = price_list[-1].extract()
    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath("//form//h1/text()").extract_first()),
        content=clean_text(response.selector.xpath("//form//dd/div/div/text()").extract_first()),
        author=clean_text(response.selector.xpath("//form//h2[1]/a/text()").extract_first()),
        editorial=clean_text(response.selector.xpath("//form//h2[2]/a/text()").extract_first()),
        price=clean_price(price),
        ISBN=clean_price(response.selector.xpath("//dd//tbody/tr[6]/td").extract_first()),
        image=response.selector.xpath('//*/img[@id="pimage"]/@src').extract_first()
    )

    if data.get("image") and "nodisponible" in data.get("image"):
        data["image"] = None

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data


def parse_details_gonvill(response):
    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath("//div/dl/h1/text()").extract_first()),
        content=clean_text(response.selector.xpath('//div/p[@itemprop="description"]/text()').extract_first()),
        author=clean_text(response.selector.xpath("//div/dl/p/a/text()").extract_first()),
        editorial=clean_text(response.selector.xpath('//div/dl/dd/a[@itemprop="publisher"]/text()').extract_first()),
        price=clean_price(response.selector.xpath('//div/span[@itemprop="price"]/text()').extract_first()),
        ISBN=clean_price(response.selector.xpath('//div//dl/dd[@itemprop="isbn"]/text()').extract_first()),
        image=response.selector.xpath('//*[@itemprop="image"]/@src').extract_first()
    )

    default_image = "https://www.gonvill.com.mx/images/NOportada.jpg"
    if data.get("image") == default_image:
        data["image"] = None

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

    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath('//div/h1[@itemprop="name"]/text()').extract_first()),
        content=clean_text(response.selector.xpath('//div[@id="productoPR_descripcion"]/text()').extract_first()),
        author=clean_text(response.selector.xpath('//div/h2[@id="productoPR_autor"]/a/text()').extract_first()),
        editorial=clean_text(response.selector.xpath('//dl/dd/a[@itemprop="publisher"]/text()').extract_first()),
        price=clean_price(response.selector.xpath('//div/p/span[@itemprop="price"]/text()').extract_first()),
        ISBN=clean_price(response.selector.xpath('//dd[@itemprop="ISBN"]/text()').extract_first()),
        image=response.selector.xpath('//img[@id="thumb1"]/@src').extract_first()
    )

    default_image = "https://i2.wp.com/pendulo.com/images/no_image_product.gif"
    if data.get("image") == default_image:
        data["image"] = None

    old_price = response.meta.get("price")
    try:
        new_price = float(data["price"])
    except ValueError:
        return

    if not old_price or new_price != old_price:
        yield data


def parse_details_porrua(response):
    isbn = response.url.split("/")[-1]
    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath("//div[@class]/strong[@style][1]/text()").extract_first()),
        content="",
        author=clean_text(response.selector.xpath('//div[@class]/p[@style][1]/span/text()').extract_first()),
        editorial=clean_text(response.selector.xpath("//div[@class]/p[@style][2]/span/text()").extract_first()),
        price=clean_price(response.selector.xpath('//div[@class="comprar_precio"]/strong/text()').extract_first()),
        ISBN=isbn,
        image=response.selector.xpath('//div[@id="librosContainer"]/div/a[@href]/img/@src').extract_first()
    )

    default_image = "https://www.porrua.mx/images/covers/na_medium.png"
    if data.get("image") == default_image:
        data["image"] = None

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
    isbn_list = response.selector.re('<span\s+class="editorial">(\d{13})<\/span>')
    if not isbn_list:
        return

    isbn = isbn_list[0]
    data = BookItem(
        url=response.url,
        title=clean_text(response.selector.xpath("//div/div/h1/text()").extract_first()),
        content=clean_text(response.selector.xpath("//div/div/section/div[1]/p/text()").extract_first()),
        author=clean_text(response.selector.xpath('//div[@class="descripcion-libro DER"]/a/text()').extract_first()),
        editorial=clean_text(response.selector.xpath("//div/div/span/a/text()").extract_first()),
        price=clean_price(response.selector.xpath('//div/div/div/p/span[2]/text()').extract_first()),
        ISBN=clean_isbn(isbn),
        image=response.selector.xpath('//img[@class="Libro"]/@src').extract_first().strip()
    )

    default_image = "https://www.elsotano.com/cover/100/5/1/200-325/no-cover/default.jpg"
    if data.get("image") == default_image:
        data["image"] = None

    if not data.get("title") or not data.get("price") or not data.get("ISBN"):
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
        return None

    return re.sub(r"[^\d\.]", "", price)


def clean_url(url):
    return re.sub(r'[%20]+$', "", url)