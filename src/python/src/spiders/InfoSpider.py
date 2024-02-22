import json

import scrapy
from scrapy.core.downloader.handlers.http11 import TunnelError

from datetime import datetime

from scrapy.spidermiddlewares.httperror import HttpError

from rmq.items import RMQItem
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import TaskToSingleResultSpider, TaskToMultipleResultsSpider
from rmq.utils import get_import_full_name, TaskStatusCodes
from rmq.utils.decorators import rmq_callback, rmq_errback
from utils import GeneratorUniqueId, ParseAddress, ParsePhoneNumber, ParseWorkHours, ParseCustomerReviews, \
    ParseManagement, ParseContactInformation, ParseSocialMedia, ParseID


class MetaInfoItem(RMQItem):
    status = scrapy.Field()
    exception = scrapy.Field()
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


def empty_metadata_info(status, error_id, description, url):
    item = MetaInfoItem()
    item['status'] = status
    item['exception'] = f"Error code: {error_id}. Description: {description}."
    item['business_id'] = ParseID().parse_id(url)
    item['business_name'] = None
    item['business_address'] = None
    item['business_category'] = None
    item['business_web_url'] = None
    item['business_img_url'] = None
    item['business_detailed_url'] = url
    item['business_phone'] = None
    item['business_fax'] = None
    item['business_hours'] = None
    item['business_stars'] = None
    item['business_customer_reviews'] = None
    item['business_bbb_rating'] = None
    item['business_accredited_date'] = None
    item['business_social_media'] = None
    item['business_years'] = None
    item['business_started_date'] = None
    item['parse_date'] = None
    item['business_contact_information'] = None
    item['business_management'] = None
    return item


class InfospiderSpider(TaskToMultipleResultsSpider):
    name = "InfoSpider"

    custom_settings = {"ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, }}

    def __init__(self, *args, **kwargs):
        super(InfospiderSpider, self).__init__(*args, **kwargs)
        self.task_queue_name = "info_spider_tasks_queue"
        self.result_queue_name = "info_spider_result_queue"
        # Пример как подключится к таске
        first_task = self.processing_tasks.get_task(delivery_tag=1)
        first_task.exception = 'Something'

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        if "sitemap_url" in data:
            return scrapy.Request(data["sitemap_url"], callback=self.parse, errback=self._errback)
        elif "business_detailed_url" in data:
            return scrapy.Request(data["business_detailed_url"], callback=self.parse, errback=self._errback)

    @rmq_callback
    def parse(self, response):
        business_id = ParseID().parse_id(response.url)
        business_detailed_url = response.url
        # business_detailed_url = response.xpath("//a[@class='dtm-read-more']/@href").extract_first()
        business_name = response.css('span.bds-h2::text').get()
        business_category = response.xpath('//h1[@class="stack"]/following-sibling::div[1]/text()').get()
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
        parse_date = datetime.strftime(datetime.now(), '%d/%m/%Y')
        yield MetaInfoItem({
            'status': TaskStatusCodes.SUCCESS.value,
            'exception': None,
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
        if failure.check(HttpError):
            status_code = failure.value.response.status
            description = str(failure.value)
            url = failure.value.response.url
            yield empty_metadata_info(TaskStatusCodes.ERROR.value, status_code, description, url)
        elif failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        else:
            self.logger.warning(f"IN ERRBACK: {repr(failure)}")

    @rmq_errback
    def _errback_second(self, failure):
        if failure.check(HttpError):
            status_code = failure.value.response.status
            description = str(failure.value)
            url = failure.value.response.url.replace("/details", "")
            yield empty_metadata_info(TaskStatusCodes.ERROR.value, status_code, description, url)
        elif failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        else:
            self.logger.warning(f"IN ERRBACK: {repr(failure)}")
