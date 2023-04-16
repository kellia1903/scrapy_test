import scrapy

from datetime import datetime

from .utilities import (assets_convert,
                        marketing_tags_convert,
                        metadata_convert,
                        price_data_convert,
                        stock_convert,
                        title_convert)
from ..constants import categories
from ..items import TestAptekaOtSkladaItem


class TestAptekaSpider(scrapy.Spider):
    name = "test_apteka"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = ["https://apteka-ot-sklada.ru/"]

    def start_requests(self):
        for category in categories.values():
            url = self.start_urls[0] + 'catalog/' + category
            yield scrapy.Request(
                url, cookies={'city': 92}, callback=self.parse_pages
            )

    def parse_pages(self, response):
        pages = response.xpath(
            '//li[@class="ui-pagination__item ui-pagination__page"]/a/@href'
        ).getall()
        url = response.url
        if pages != []:
            for href in pages:
                url = response.urljoin(href)
                yield response.follow(
                    url, cookies={'city': 92}, callback=self.parse
                )
        yield response.follow(
            url, cookies={'city': 92}, callback=self.parse, dont_filter=True
        )

    def parse(self, response):
        all_on_page = response.xpath(
            '//a[@class="goods-card__link"]/@href'
            ).getall()
        for href_of_product in all_on_page:
            url = response.urljoin(href_of_product)
            yield response.follow(
                url, cookies={'city': 92}, callback=self.parse_product
            )

    def parse_product(self, response):

        data = {
            "timestamp": datetime.now().timestamp(),
            "RPC": response.url.split('_')[-1],
            "url": response.url,
            "title": title_convert(response),
            "marketing_tags": marketing_tags_convert(response),
            "brand": response.xpath(
                        '//span[@itemtype="legalName"]/text()'
                    ).get(),
            "section": response.xpath(
                        '//span[@itemprop="name"]/text()'
                    ).getall()[2:-2],
            "price_data": price_data_convert(response),
            "stock": stock_convert(response),
            "assets": assets_convert(response),
            "metadata": metadata_convert(response),
            "variants": 1,
        }
        yield TestAptekaOtSkladaItem(data)
