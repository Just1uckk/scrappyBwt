from sqlalchemy.dialects.mysql import insert

from database.models.sitemap_model import SitemapModel
from rmq.commands import Consumer
from rmq.utils import TaskStatusCodes


class SitemapPagesResultConsumer(Consumer):

    def init_queue_name(self, opts):
        self.queue_name = queue_name = self.settings.get("RABBITMQ_SITEMAP_RESULTS")
        return queue_name

    def build_message_store_stmt(self, message_body):
        message_body['status'] = TaskStatusCodes.SUCCESS.value
        stmt = insert(SitemapModel)
        stmt = stmt.on_duplicate_key_update({
            'status': stmt.inserted.status
        }).values({
            "sitemap_url": message_body['url']
        })
        return stmt
