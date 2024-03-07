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
    phone = Column(BIGINT(unsigned=True), index=True)
    fax = Column(BIGINT(unsigned=True), index=True)
    hours = Column(JSON)
    stars = Column(VARCHAR(255))
    customer_reviews = Column(VARCHAR(255))
    bbb_rating = Column(VARCHAR(255))
    accredited_date = Column(VARCHAR(255))
    social_media = Column(JSON)
    years = Column(VARCHAR(255))
    started_date = Column(VARCHAR(255))
    parse_date = Column(VARCHAR(255))
    contact_information = Column(JSON)
    management = Column(JSON)
    sent_to_customer = Column(VARCHAR(255))

