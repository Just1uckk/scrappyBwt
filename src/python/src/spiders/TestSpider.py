import json

import scrapy

from utils import ParseWorkHours, ParseCustomerReviews


class TestspiderSpider(scrapy.Spider):
    name = "TestSpider"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://www.bbb.org/us/ca/san-jose/profile/new-car-dealers/capitol-toyotascion-1216-198833"]

    def parse(self, response):
        # business_stars = response.css('div.dtm-stars + *::text').get()
        business_bbb_rating = response.css('span.dtm-rating span span::text').getall()
        print(business_bbb_rating)
        pass
