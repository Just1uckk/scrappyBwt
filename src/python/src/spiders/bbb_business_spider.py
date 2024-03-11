import json

import scrapy
from scrapy.utils.project import get_project_settings
from datetime import datetime

from items.info_business_item import InfoBusinessItem
from middlewares import BlockedRetryMiddleware
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import TaskToMultipleResultsSpider
from rmq.utils import get_import_full_name, TaskStatusCodes
from rmq.utils.decorators import rmq_callback, rmq_errback
from utils import ParseAddress, ParsePhoneNumber, ParseWorkHours, ParseCustomerReviews, \
    ParseManagement, ParseContactInformation, ParseSocialMedia, ParseID, ParseCategories


class BBBBusinessSpider(TaskToMultipleResultsSpider):
    name = "bbb_business_spider"

    custom_settings = {
        "ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, },
    }

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        downloader_middlewares = settings.get("DOWNLOADER_MIDDLEWARES")
        downloader_middlewares[get_import_full_name(BlockedRetryMiddleware)] = 500
        settings.set("DOWNLOADER_MIDDLEWARES", downloader_middlewares)

    def __init__(self, *args, **kwargs):
        super(BBBBusinessSpider, self).__init__(*args, **kwargs)
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
        bbb_id = ParseID().parse_id(response.url)
        detailed_url = response.xpath("//a[@class='dtm-read-more']/@href").extract_first()
        name = response.xpath('//span[contains(@class,"bds-h2")]/text()').get()
        category = ParseCategories().parse_categories(response)
        address = ParseAddress().parse_address(
            response.xpath('//address//p[contains(@class, "bds-body")]/text()').getall())
        web_url = response.xpath('//a[@class="dtm-url"]/@href').extract_first()
        img_url = response.xpath('//div[contains(@class, "dtm-logo")]//img/@src').extract_first()
        phone = ParsePhoneNumber().clean_phone_number(response.xpath('//a[@class="dtm-phone"]/text()').get())
        hours = ParseWorkHours().parse_work_hours(response)
        stars = response.xpath('//div[contains(@class, "dtm-stars")]/following-sibling::*[1]/text()').get()
        customer_reviews = ParseCustomerReviews().parse_customer_reviews(response)
        bbb_rating = response.xpath('//span[contains(@class, "dtm-rating")]//span//span/text()').get()
        more_details_url = response.xpath('//a[@class="dtm-read-more"]/@href').extract_first()
        meta_info = {
            'bbb_id': bbb_id,
            'name': name,
            'category': category,
            'address': address,
            'detailed_url': detailed_url,
            'web_url': web_url,
            'img_url': img_url,
            'phone': phone,
            'hours': hours,
            'stars': stars,
            'customer_reviews': customer_reviews,
            'bbb_rating': bbb_rating,
        }
        yield scrapy.Request(url=more_details_url,
                             callback=self.get_info_from_detailed_page, meta=meta_info, errback=self._errback_second)

    @rmq_callback
    def get_info_from_detailed_page(self, response):
        accredited_date = response.xpath(
            '//dt[contains(text(),"Accredited Since")]/following-sibling::dd[1]/text()').get()
        if accredited_date is not None:
            try:
                accredited_date = datetime.strptime(accredited_date, "%m/%d/%Y")
                accredited_date = accredited_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                accredited_date = datetime.strptime(accredited_date, "%d/%m/%Y")
                accredited_date = accredited_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        started_date = response.xpath(
            '//dt[contains(text(),"Business Started")]/following-sibling::dd[1]/text()').get()
        if started_date is not None:
            try:
                started_date = datetime.strptime(started_date, "%m/%d/%Y")
                started_date = started_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                started_date = datetime.strptime(started_date, "%d/%m/%Y")
                started_date = started_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        years = response.xpath(
            '//dt[contains(text(),"Years in Business")]/following-sibling::dd[1]/text()').get()
        social_media = ParseSocialMedia().parse_social_media(response)
        fax = ParsePhoneNumber().clean_phone_number(response.xpath(
            '//div[contains(text(),"Primary Fax")]/preceding-sibling::span[1]/text()').get())
        management = ParseManagement().parse_management(response)
        contact_information = ParseContactInformation().parse_contact_information(response)
        parse_date = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.logger.info(f"Business: {response.meta['name']}. Parsed successfully: {parse_date}.")
        yield InfoBusinessItem({
            'bbb_id': response.meta['bbb_id'],
            'name': response.meta['name'],
            'category': response.meta['category'],
            'address': response.meta['address'],
            'detailed_url': response.meta['detailed_url'],
            'web_url': response.meta['web_url'],
            'img_url': response.meta['img_url'],
            'phone': response.meta['phone'],
            'hours': response.meta['hours'],
            'stars': response.meta['stars'],
            'customer_reviews': response.meta['customer_reviews'],
            'bbb_rating': response.meta['bbb_rating'],
            'fax': fax,
            'accredited_date': accredited_date,
            'social_media': social_media,
            'years': years,
            'started_date': started_date,
            'parse_date': parse_date,
            'contact_information': contact_information,
            'management': management
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
