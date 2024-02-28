from sqlalchemy.dialects.mysql import insert
from scrapy.utils.project import get_project_settings

from database.models.sitemap_pages import SitemapPages
from rmq.commands import Consumer
from rmq.utils import TaskStatusCodes


class SitemapPagesResultConsumer(Consumer):

    def init_queue_name(self, opts):
        self.project_settings = get_project_settings()
        self.queue_name = queue_name = self.project_settings.get("RABBITMQ_SITEMAP_RESULTS")
        return queue_name

    def build_message_store_stmt(self, message_body):
        message_body['status'] = TaskStatusCodes.SUCCESS.value
        stmt = insert(SitemapPages)
        stmt = stmt.on_duplicate_key_update({
            'status': stmt.inserted.status
        }).values({
            "sitemap_url": message_body['url']
        })
        return stmt
