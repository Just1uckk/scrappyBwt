import scrapy

from rmq.items import RMQItem


class SitemapItem(RMQItem):
    url = scrapy.Field()
