import scrapy
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.utils.project import get_project_settings

from items.sitemap_item import SitemapItem
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import HttpbinSpider
from rmq.utils import get_import_full_name
from rmq.utils.decorators import rmq_callback, rmq_errback


class BBBSitemapSpider(HttpbinSpider):
    name = "bbb_sitemap_spider"

    custom_settings = {"ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310, }}

    def __init__(self, *args, **kwargs):
        super(BBBSitemapSpider, self).__init__(*args, **kwargs)
        self.project_settings = get_project_settings()
        self.result_queue_name = self.project_settings.get("RABBITMQ_SITEMAP_RESULTS")

    def start_requests(self):
        yield scrapy.Request("https://www.bbb.org/sitemap-accredited-business-profiles-index.xml",
                             callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        for url in response.xpath('//*[local-name()="loc"]/text()').getall():
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//*[local-name()="loc"]/text()').getall():
            self.logger.info(f'Sitemap url: {url} parsed successfully.')
            yield SitemapItem({'url': url})

    @rmq_errback
    def _errback(self, failure):
        if failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        else:
            self.logger.warning(f"IN ERRBACK: {repr(failure)}")
