from sqlalchemy.sql.schema import Column

from .base import Base
from .mixins import (
    MysqlPriorityAttemptMixin,
    MysqlExceptionMixin,
    MysqlStatusMixin,
    MysqlTimestampsMixin,
    MysqlPrimaryKeyMixin,
)
from sqlalchemy.dialects.mysql import TEXT


class SitemapModel(
    Base,
    MysqlPrimaryKeyMixin,
    MysqlStatusMixin,
    MysqlTimestampsMixin,
    MysqlPriorityAttemptMixin,
    MysqlExceptionMixin
):
    __tablename__ = 'sitemap_model'

    sitemap_url = Column(TEXT, nullable=False, index=True)
