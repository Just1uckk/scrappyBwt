from argparse import Namespace

from sqlalchemy import select, update, text, and_

from database.models.info_page import InfoPage
from rmq.commands import Producer
from rmq.utils import TaskStatusCodes


class InfoPagesRepliesProducer(Producer):
    # def __init__(self):
    #     super().__init__()
    #     self.task_queue_name = 'info_spider_tasks_queue'
    #     self.reply_queue_name = 'info_spider_replies_queue'
    #     self.max_attempts = 3
    MAX_ATTEMPTS = 3

    def init_replies_queue(self, opts: Namespace):
        self.task_queue_name = 'info_spider_tasks_queue'

    def init_replies_queue_name(self, opts: Namespace):
        self.task_queue_name = 'info_spider_replies_queue'

    def build_task_query_stmt(self, chunk_size):
        stmt = select([InfoPage]).where(
            and_(
                InfoPage.status == TaskStatusCodes.ERROR.value,
                InfoPage.attempt < self.MAX_ATTEMPTS,
            )
        ).order_by(InfoPage.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        return update(InfoPage).where(
            InfoPage.id == db_task["id"]
        ).values({
            "status": TaskStatusCodes.IN_QUEUE.value,
            "attempt": text("attempt + 1")
        })
