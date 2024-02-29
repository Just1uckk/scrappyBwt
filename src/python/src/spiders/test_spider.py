import json

import scrapy

from utils import ParseWorkHours, ParseCustomerReviews, ParseManagement, ParseSocialMedia, ParseID


class TestSpider(scrapy.Spider):
    name = "test_spider"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://www.bbb.org/us/ca/san-rafael/profile/auto-repair/peruva-auto-repair-service-1116-417396"]

    def parse(self, response):
        business_accredited_date = response.xpath(
            '//dt[contains(text(),"Accredited Since")]/following-sibling::dd[1]/text()').get()
        pass
