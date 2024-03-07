import json
import scrapy
from utils import ParseWorkHours, ParseCustomerReviews, ParseManagement, ParseSocialMedia, ParseID, ParseAddress



class TestSpider(scrapy.Spider):
    name = "test_spider"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://www.bbb.org/us/ca/san-francisco/profile/auto-body-repair-and-painting/lombard-auto-body-llc-1116-458274"]

    def parse(self, response):
        test = response.xpath(
            '//dt[contains(text(),"Accredited Since")]/following-sibling::dd[1]/text()').get()
        print('BUSINESS ACCREDITED DATE')
        print(test)
        pass
