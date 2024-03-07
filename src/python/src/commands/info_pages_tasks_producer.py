from sqlalchemy import select, update, text, and_, or_
from scrapy.utils.project import get_project_settings

from database.models.sitemap_pages import SitemapPages
from rmq.commands import Producer
from rmq.utils import TaskStatusCodes


class InfoPagesTasksProducer(Producer):
    def __init__(self):
        super().__init__()
        self.project_settings = get_project_settings()
        self.task_queue_name = self.project_settings.get("RABBITMQ_INFO_TASKS")
        self.reply_to_queue_name = self.project_settings.get("RABBITMQ_INFO_REPLIES")
        self.max_attempts = 3

    def build_task_query_stmt(self, chunk_size):
        stmt = select([SitemapPages.id, SitemapPages.status, SitemapPages.attempt, SitemapPages.sitemap_url]).where(
            and_(
                or_(SitemapPages.status == TaskStatusCodes.NOT_PROCESSED.value,
                    SitemapPages.status == TaskStatusCodes.ERROR.value),
                SitemapPages.attempt < self.max_attempts,
                ),
            ).order_by(SitemapPages.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        return update(SitemapPages).where(
            SitemapPages.id == db_task["id"]
        ).values({
            "status": TaskStatusCodes.IN_QUEUE.value,
            "attempt": text("attempt + 1")
        })
