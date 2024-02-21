from sqlalchemy import select

from database.models.sitemap_pages import SitemapPages
from rmq.commands import Producer
from rmq.utils import TaskStatusCodes


class InfoPagesTasksProducer(Producer):
    def __init__(self):
        super().__init__()
        self.task_queue_name = 'info_spider_tasks_queue'

    def build_task_query_stmt(self, chunk_size):
        stmt = select([SitemapPages]).where(
            SitemapPages.status == TaskStatusCodes.NOT_PROCESSED.value,
        ).order_by(SitemapPages.id.asc()).limit(chunk_size)
        return stmt
