import json

import scrapy

from utils import ParseWorkHours, ParseCustomerReviews, ParseManagement, ParseSocialMedia


class TestspiderSpider(scrapy.Spider):
    name = "TestSpider"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://www.bbb.org/us/ca/sausalito/profile/food-manufacturer/california-caviar-company-1116-316068/details"]

    def parse(self, response):
        business_social_media = ParseSocialMedia().parse_social_media(response)
        print(business_social_media)
        pass
