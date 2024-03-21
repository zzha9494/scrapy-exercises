import scrapy
from scrapy.http import JsonRequest
from scrapy.exceptions import CloseSpider
from scrapy.item import Item, Field


class SurfboardEmpireProduct(Item):
    sku_name = Field()
    product_id = Field()
    brand = Field()
    product_url = Field()


class SurfboardEmpireSpider(scrapy.Spider):
    name = 'surfboardempire'
    start_urls = ['https://www.surfboardempire.com.au/products.json?page=1']
    page_num = 1
    base_url = 'https://www.surfboardempire.com.au/products.json?page={}'

    def parse(self, response):
        """
        Please note there is no url field in json response.
        """
        try:
            data = response.json()
            products = data.get('products', [])
        except Exception as e:
            self.logger.error(
                f"Error parsing JSON data on page {self.page_num}: {e}")
            raise CloseSpider(f"Invalid JSON received on page {self.page_num}")

        if not products:
            return

        self.logger.info(f"Now processing page {self.page_num}")

        for product in products:
            yield self.parse_product(product)

        self.page_num += 1
        next_page_url = self.base_url.format(self.page_num)
        yield response.follow(next_page_url, callback=self.parse)

    def parse_product(self, product):
        product_item = SurfboardEmpireProduct()

        product_item["sku_name"] = product.get('title')
        product_item["product_id"] = product.get('id')
        product_item["brand"] = product.get('vendor')
        product_item["product_url"] = product.get('url')

        return product_item
