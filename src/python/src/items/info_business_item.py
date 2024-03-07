import scrapy

from rmq.items import RMQItem


class InfoBusinessItem(RMQItem):
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
