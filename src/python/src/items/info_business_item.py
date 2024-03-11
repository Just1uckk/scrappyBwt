import scrapy

from rmq.items import RMQItem


class InfoBusinessItem(RMQItem):
    bbb_id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    category = scrapy.Field()
    web_url = scrapy.Field()
    img_url = scrapy.Field()
    detailed_url = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    hours = scrapy.Field()
    stars = scrapy.Field()
    customer_reviews = scrapy.Field()
    bbb_rating = scrapy.Field()
    accredited_date = scrapy.Field()
    social_media = scrapy.Field()
    years = scrapy.Field()
    started_date = scrapy.Field()
    parse_date = scrapy.Field()
    contact_information = scrapy.Field()
    management = scrapy.Field()
