import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.item import Item, Field


class TackleWorldProduct(Item):
    sku_name = Field()
    image_url = Field()
    price_now = Field()
    price_was = Field()
    product_url = Field()


class TackleWorldSpider(scrapy.Spider):
    name = "tackleworldadelaide"
    allowed_domains = ["tackleworldadelaide.com.au"]
    start_urls = ["https://tackleworldadelaide.com.au/"]

    def parse(self, response):
        """
        Navigates through the top level-menu (e.g., Reels, Rods, etc.) 
        and loops through the submenu items within.
        Although those submenu items can be selected directly using their class name, 
        these steps follow the provided instructions.
        """

        # Navigate through the top level-menu
        try:
            top_menu_xpath = '//ul[contains(@class, "navPages-list--categories")]/li'
            top_menu_items = response.xpath(top_menu_xpath)
        except Exception as e:
            self.logger.error(f"Error parsing top menu: {e}")
            raise CloseSpider("Failed to parse top menu")

        # Loop through each item in the top menu
        for top_menu_item in top_menu_items:
            sub_menu_xpaths = './/li[@class="navPage-subMenu-item"]'
            sub_menu_items = top_menu_item.xpath(sub_menu_xpaths)

            # Loop through each sub item
            for category in sub_menu_items:
                try:
                    category_link = category.xpath(
                        './/a[contains(@class, "navPage-subMenu-action")]//@href').get()
                except Exception as e:
                    self.logger.error(f"Error parsing category link: {e}")
                    continue

                # Visit the category page
                if category_link:
                    self.logger.info(f"Processing category at {category_link}")
                    yield scrapy.Request(category_link, callback=self.parse_products)

    def parse_products(self, response):
        """
        Please note the price field is stored as string without removing "AUD $"
        """
        # Get the next page url
        next_page_xpath = '//li[contains(@class, "pagination__item--next")]/a/@href'
        next_page_link = response.xpath(next_page_xpath).get()

        # Extract product tiles
        products_xpath = '//li[@class="product"]'
        products = response.xpath(products_xpath)

        for product in products:
            # Extract product details
            product_item = TackleWorldProduct()
            try:
                product_item["sku_name"] = product.xpath(
                    './/h4[@class="card-title"]/a/text()').get()
                product_item["image_url"] = product.xpath(
                    './/img[@class="card-image "]/@src').get()
                product_item["price_now"] = product.xpath(
                    './/span[@class="price"]/text()').get()
                product_item["price_was"] = product.xpath(
                    './/span[@class="price price--rrp"]/text()').get()
                product_item["product_url"] = product.xpath(
                    './/h4[@class="card-title"]/a/@href').get()
            except Exception as e:
                self.logger.error(f"Error parsing product details: {e}")
                continue

            yield product_item

        # Go to the next page if it exists
        if next_page_link:
            yield scrapy.Request(next_page_link, callback=self.parse_products)
