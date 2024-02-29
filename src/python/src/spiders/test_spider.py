import json
import scrapy
from utils import ParseWorkHours, ParseCustomerReviews, ParseManagement, ParseSocialMedia, ParseID, ParseAddress



class TestSpider(scrapy.Spider):
    name = "test_spider"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://www.bbb.org/us/tx/san-antonio/profile/auto-repair/dynamic-car-service-0825-90105933"]

    def parse(self, response):
        test = ParseCategories().parse_categories(response)
        pass
