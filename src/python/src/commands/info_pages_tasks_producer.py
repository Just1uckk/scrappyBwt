from sqlalchemy import select, update, text

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

    def build_task_update_stmt(self, db_task, status):
        return update(SitemapPages).where(
            SitemapPages.id == db_task["id"]
        ).values({
            "status": TaskStatusCodes.IN_QUEUE.value,
            "attempt": text("attempt + 1")
        })
