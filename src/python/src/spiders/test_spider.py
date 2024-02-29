import json

import scrapy

from utils import ParseWorkHours, ParseCustomerReviews, ParseManagement, ParseSocialMedia, ParseID, ParseCategories


class TestSpider(scrapy.Spider):
    name = "test_spider"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://www.bbb.org/us/ca/san-rafael/profile/auto-repair/peruva-auto-repair-service-1116-417396"]

    def parse(self, response):
        test = ParseCategories().parse_categories(response)
        print(test)
        pass
