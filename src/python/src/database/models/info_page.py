from sqlalchemy import VARCHAR
from sqlalchemy.dialects.mssql import JSON
from sqlalchemy.sql.schema import Column

from .base import Base
from .mixins import (
    MysqlPriorityAttemptMixin,
    MysqlExceptionMixin,
    MysqlStatusMixin,
    MysqlTimestampsMixin,
    MysqlPrimaryKeyMixin,
)
from sqlalchemy.dialects.mysql import TEXT, INTEGER, BIGINT, MEDIUMINT


class InfoPage(
    Base,
    MysqlPrimaryKeyMixin,
    # MysqlStatusMixin,
    MysqlTimestampsMixin,
    # MysqlPriorityAttemptMixin,
    # MysqlExceptionMixin
):
    __tablename__ = 'info_page'

    bbb_id = Column(VARCHAR(255), index=True, unique=True, nullable=False)
    name = Column(TEXT)
    address = Column(VARCHAR(768))
    category = Column(TEXT)
    web_url = Column(VARCHAR(768))
    img_url = Column(VARCHAR(768))
    detailed_url = Column(VARCHAR(768), nullable=False)
    phone = Column(BIGINT, index=True)
    fax = Column(BIGINT, index=True)
    hours = Column(JSON)
    stars = Column(VARCHAR)
    customer_reviews = Column(VARCHAR)
    bbb_rating = Column(VARCHAR)
    accredited_date = Column(VARCHAR)
    social_media = Column(JSON)
    years = Column(VARCHAR)
    started_date = Column(VARCHAR)
    parse_date = Column(VARCHAR)
    contact_information = Column(JSON)
    management = Column(JSON)
    sent_to_customer = Column(VARCHAR)

