from sqlalchemy import Column

from base import Base
from mixins import *
from sqlalchemy.dialects.mysql import TEXT


class SitemapPages(
    Base,
    MysqlPrimaryKeyMixin,
    MysqlStatusMixin,
    MysqlTimestampsMixin,
    MysqlPriorityAttemptMixin,
    MysqlExceptionMixin
):
    __tablename__ = 'sitemap_pages'

    sitemap_url = Column(TEXT, nullable=False)
