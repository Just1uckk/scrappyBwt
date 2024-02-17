import base64
import hashlib
import json
from urllib.parse import urlparse

import scrapy
from scrapy.core.downloader.handlers.http11 import TunnelError

from rmq.items import RMQItem
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import TaskToSingleResultSpider
from rmq.utils import get_import_full_name
from rmq.utils.decorators import rmq_callback, rmq_errback
from utils import GeneratorUniqueId, ParseAddress, ParsePhoneNumber, ParseWorkHours, ParseCustomerReviews


class MetaInfoItem(RMQItem):
    business_id = scrapy.Field()
    business_name = scrapy.Field()
    business_address = scrapy.Field()
    business_category = scrapy.Field()
    business_web_url = scrapy.Field()
    business_img_url = scrapy.Field()
    business_phone = scrapy.Field()
    business_fax = scrapy.Field()
    business_hours = scrapy.Field()
    business_stars = scrapy.Field()
    business_customer_reviews = scrapy.Field()
    business_bbb_rating = scrapy.Field()
    business_detailed_url = scrapy.Field()

# class AdressField:
#     def __init__(self,full_adress,)

class InfospiderSpider(TaskToSingleResultSpider):
    name = "InfoSpider"

    # custom_settings = {"ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, }}

    def __init__(self, *args, **kwargs):
        super(InfospiderSpider, self).__init__(*args, **kwargs)
        self.task_queue_name = "SitemapSpider_result_queue"
        self.result_queue_name = f"{self.name}_result_queue"

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return scrapy.Request(data["url"], callback=self.parse)

    @rmq_callback
    def parse(self, response):
        business_id = GeneratorUniqueId().string_to_unique_id(response.url)
        business_detailed_url = response.xpath("//a[@class='dtm-read-more']/@href").extract_first()
        business_name = response.css('span.bds-h2::text').get()
        business_category = response.xpath('//h1[@class="stack"]/following-sibling::div[1]/text()').get()
        business_address = ParseAddress().parse_address(response.css('address p.bds-body::text').getall())
        business_web_url = response.xpath('//a[@class="dtm-url"]/@href').extract_first()
        business_img_url = response.css('div.dtm-logo img::attr(src)').extract_first()
        business_phone = ParsePhoneNumber().clean_phone_number(response.xpath('//a[@class="dtm-phone"]/text()').get())
        business_fax = None # Question to Igor
        business_hours = ParseWorkHours().parse_work_hours(response)
        business_stars = response.css('div.dtm-stars + *::text').get()
        business_customer_reviews = ParseCustomerReviews().parse_customer_reviews(response)
        business_bbb_rating = response.css('span.dtm-rating span span::text').get()

        # print(MetaInfoItem({
        #     'business_id': business_id,
        #     'business_name': business_name,
        #     'business_address': business_address,
        #     'business_detailed_url': business_detailed_url,
        #     'business_web_url': business_web_url,
        #     'business_img_url': business_img_url,
        #     'business_phone': business_phone,
        #     'business_fax': business_fax,
        #     'business_hours': business_hours,
        #     'business_stars': business_stars,
        #     'business_customer_reviews': business_customer_reviews,
        #     'business_bbb_rating': business_bbb_rating,
        # }))
        print(response.url)
        yield MetaInfoItem({
            'business_id': business_id,
            'business_name': business_name,
            'business_category': business_category,
            'business_address': business_address,
            'business_detailed_url': business_detailed_url,
            'business_web_url': business_web_url,
            'business_img_url': business_img_url,
            'business_phone': business_phone,
            'business_fax': business_fax,
            'business_hours': business_hours,
            'business_stars': business_stars,
            'business_customer_reviews': business_customer_reviews,
            'business_bbb_rating': business_bbb_rating,
        })

    @rmq_errback
    def _errback(self, failure):
        if failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        else:
            self.logger.warning(f"IN ERRBACK: {repr(failure)}")
