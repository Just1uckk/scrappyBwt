from sqlalchemy import update

from database.models.sitemap_pages import SitemapPages
from rmq.commands import Consumer
from scrapy.utils.project import get_project_settings


class InfoPagesRepliesConsumer(Consumer):
    def init_queue_name(self, opts):
        self.project_settings = get_project_settings()
        self.queue_name = queue_name = self.project_settings.get("RABBITMQ_INFO_REPLIES")
        return queue_name

    def build_message_store_stmt(self, message_body):
        return update(
            SitemapPages
        ).where(
            SitemapPages.id == message_body['id']
        ).values({
            'status': message_body['status'],
            "exception": message_body['exception']
        })
