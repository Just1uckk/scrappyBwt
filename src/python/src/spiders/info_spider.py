import json

import scrapy
from scrapy.utils.project import get_project_settings
from datetime import datetime

from rmq.items import RMQItem
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import TaskToMultipleResultsSpider
from rmq.utils import get_import_full_name, TaskStatusCodes
from rmq.utils.decorators import rmq_callback, rmq_errback
from utils import ParseAddress, ParsePhoneNumber, ParseWorkHours, ParseCustomerReviews, \
    ParseManagement, ParseContactInformation, ParseSocialMedia, ParseID, ParseCategories


class MetaInfoItem(RMQItem):
    business_id = scrapy.Field()
    business_name = scrapy.Field()
    business_address = scrapy.Field()
    business_category = scrapy.Field()
    business_web_url = scrapy.Field()
    business_img_url = scrapy.Field()
    business_detailed_url = scrapy.Field()
    business_phone = scrapy.Field()
    business_fax = scrapy.Field()
    business_hours = scrapy.Field()
    business_stars = scrapy.Field()
    business_customer_reviews = scrapy.Field()
    business_bbb_rating = scrapy.Field()
    business_accredited_date = scrapy.Field()
    business_social_media = scrapy.Field()
    business_years = scrapy.Field()
    business_started_date = scrapy.Field()
    parse_date = scrapy.Field()
    business_contact_information = scrapy.Field()
    business_management = scrapy.Field()

class InfoSpider(TaskToMultipleResultsSpider):
    name = "info_spider"

    custom_settings = {"ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, }}

    def __init__(self, *args, **kwargs):
        super(InfoSpider, self).__init__(*args, **kwargs)
        self.project_settings = get_project_settings()
        self.task_queue_name = self.project_settings.get("RABBITMQ_INFO_TASKS")
        self.result_queue_name = self.project_settings.get("RABBITMQ_INFO_RESULTS")

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        if "sitemap_url" in data:
            return scrapy.Request(data["sitemap_url"], callback=self.parse, errback=self._errback)
        elif "business_detailed_url" in data:
            return scrapy.Request(data["business_detailed_url"], callback=self.parse, errback=self._errback)

    @rmq_callback
    def parse(self, response):
        business_id = ParseID().parse_id(response.url)
        business_detailed_url = response.xpath("//a[@class='dtm-read-more']/@href").extract_first()
        business_name = response.css('span.bds-h2::text').get()
        business_category = ParseCategories().parse_categories(response)
        business_address = ParseAddress().parse_address(response.css('address p.bds-body::text').getall())
        business_web_url = response.xpath('//a[@class="dtm-url"]/@href').extract_first()
        business_img_url = response.css('div.dtm-logo img::attr(src)').extract_first()
        business_phone = ParsePhoneNumber().clean_phone_number(response.xpath('//a[@class="dtm-phone"]/text()').get())
        business_hours = ParseWorkHours().parse_work_hours(response)
        business_stars = response.css('div.dtm-stars + *::text').get()
        business_customer_reviews = ParseCustomerReviews().parse_customer_reviews(response)
        business_bbb_rating = response.css('span.dtm-rating span span::text').get()
        more_details_url = response.xpath('//a[@class="dtm-read-more"]/@href').extract_first()
        meta_info = {
            'business_id': business_id,
            'business_name': business_name,
            'business_category': business_category,
            'business_address': business_address,
            'business_detailed_url': business_detailed_url,
            'business_web_url': business_web_url,
            'business_img_url': business_img_url,
            'business_phone': business_phone,
            'business_hours': business_hours,
            'business_stars': business_stars,
            'business_customer_reviews': business_customer_reviews,
            'business_bbb_rating': business_bbb_rating,
        }
        yield scrapy.Request(url=more_details_url,
                             callback=self.get_info_from_detailed_page, meta=meta_info, errback=self._errback_second)

    @rmq_callback
    def get_info_from_detailed_page(self, response):
        business_accredited_date = response.xpath(
            '//dt[contains(text(),"Accredited Since")]/following-sibling::dd[1]/text()').get()
        business_started_date = response.xpath(
            '//dt[contains(text(),"Business Started")]/following-sibling::dd[1]/text()').get()
        business_years = response.xpath(
            '//dt[contains(text(),"Years in Business")]/following-sibling::dd[1]/text()').get()
        business_social_media = ParseSocialMedia().parse_social_media(response)
        business_fax = ParsePhoneNumber().clean_phone_number(response.xpath(
            '//div[contains(text(),"Primary Fax")]/preceding-sibling::span[1]/text()').get())
        business_management = ParseManagement().parse_management(response)
        business_contact_information = ParseContactInformation().parse_contact_information(response)
        parse_date = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S.%fZ')
        yield MetaInfoItem({
            'business_id': response.meta['business_id'],
            'business_name': response.meta['business_name'],
            'business_category': response.meta['business_category'],
            'business_address': response.meta['business_address'],
            'business_detailed_url': response.meta['business_detailed_url'],
            'business_web_url': response.meta['business_web_url'],
            'business_img_url': response.meta['business_img_url'],
            'business_phone': response.meta['business_phone'],
            'business_hours': response.meta['business_hours'],
            'business_stars': response.meta['business_stars'],
            'business_customer_reviews': response.meta['business_customer_reviews'],
            'business_bbb_rating': response.meta['business_bbb_rating'],
            'business_fax': business_fax,
            'business_accredited_date': business_accredited_date,
            'business_social_media': business_social_media,
            'business_years': business_years,
            'business_started_date': business_started_date,
            'parse_date': parse_date,
            'business_contact_information': business_contact_information,
            'business_management': business_management
        })

    @rmq_errback
    def _errback(self, failure):
        delivery_tag = failure.request.meta["delivery_tag"]
        status_code = failure.value.response.status
        description = str(failure.value)
        self.logger.error(f'Code: {status_code}. Description: {description}')
        self.processing_tasks.set_status(delivery_tag, TaskStatusCodes.ERROR.value)
        self.processing_tasks.set_exception(delivery_tag, f'Code: {status_code}. Description: {description}')


    @rmq_errback
    def _errback_second(self, failure):
        delivery_tag = failure.request.meta["delivery_tag"]
        status_code = failure.value.response.status
        description = str(failure.value)
        self.logger.error(f'Code: {status_code}. Description: {description}')
        self.processing_tasks.set_status(delivery_tag, TaskStatusCodes.ERROR.value)
        self.processing_tasks.set_exception(delivery_tag, f'Code: {status_code}. Description: {description}')

