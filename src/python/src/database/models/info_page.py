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
    MysqlStatusMixin,
    MysqlTimestampsMixin,
    MysqlPriorityAttemptMixin,
    MysqlExceptionMixin
):
    __tablename__ = 'info_page'

    business_id = Column(BIGINT, primary_key=True, index=True, unique=True, nullable=False)
    business_name = Column(TEXT, nullable=False)
    business_address = Column(VARCHAR(255))
    business_category = Column(TEXT, nullable=False)
    business_web_url = Column(VARCHAR(768))
    business_img_url = Column(VARCHAR(768))
    business_detailed_url = Column(VARCHAR(768), nullable=False)
    business_phone = Column(INTEGER, index=True)
    business_fax = Column(INTEGER, index=True)
    business_hours = Column(JSON)
    business_stars = Column(VARCHAR)
    business_customer_reviews = Column(VARCHAR)
    business_bbb_rating = Column(VARCHAR)
    business_accredited_date = Column(VARCHAR)
    business_social_media = Column(JSON)
    business_years = Column(VARCHAR)
    business_started_date = Column(VARCHAR)
    parse_date = Column(VARCHAR)
    business_contact_information = Column(JSON)
    business_management = Column(JSON)

