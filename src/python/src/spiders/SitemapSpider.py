import scrapy
from scrapy import Selector
from scrapy.core.downloader.handlers.http11 import TunnelError

from rmq.items import RMQItem
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import HttpbinSpider
from rmq.utils import get_import_full_name
from rmq.utils.decorators import rmq_callback, rmq_errback


class MetaUrlItem(RMQItem):
    url = scrapy.Field()


def decode_util(response):
    decoded_body = Selector(text=response.body.decode('utf-8'))
    return decoded_body


class SitemapspiderSpider(HttpbinSpider):
    name = "SitemapSpider"

    custom_settings = {"ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, }}

    def __init__(self, *args, **kwargs):
        super(SitemapspiderSpider, self).__init__(*args, **kwargs)
        self.result_queue_name = f"{self.name}_result_queue"

    def start_requests(self):
        yield scrapy.Request("https://www.bbb.org/sitemap-business-profiles-index.xml", callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        selector = decode_util(response)
        urls = selector.xpath('//loc/text()').extract()
        for loc in urls:
            yield scrapy.Request(loc, callback=self.parse)

    @rmq_callback
    def parse(self, response):
        selector = decode_util(response)
        urls = selector.xpath('//loc/text()').extract()
        for loc in urls:
            self.logger.critical(loc)
            yield MetaUrlItem({'url': loc})

    @rmq_errback
    def _errback(self, failure):
        if failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        else:
            self.logger.warning(f"IN ERRBACK: {repr(failure)}")
