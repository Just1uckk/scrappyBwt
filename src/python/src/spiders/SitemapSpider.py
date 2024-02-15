import scrapy
from scrapy import Selector
from scrapy.exceptions import CloseSpider
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor

from rmq.spiders import TaskBaseSpider, HttpbinSpider

class SitemapspiderSpider(HttpbinSpider):
    name = "SitemapSpider"

    def start_requests(self):
        yield scrapy.Request("https://www.bbb.org/sitemap-business-profiles-index.xml", callback=self.parse_sitemap, dont_filter=True)

    def decode_util(self, response):
        sel = Selector(text=response.body.decode('utf-8'))
        return sel

    def parse_sitemap(self, response):
        selector = self.decode_util(response)
        urls = selector.xpath('//loc/text()').extract()
        for loc in urls:
            yield scrapy.Request(loc, callback=self.parse_page)

    def parse_page(self, response):
        selector = self.decode_util(response)
        urls = selector.xpath('//loc/text()').extract()
        for loc in urls:
            print(loc)
            yield {
                'url': loc
            }

