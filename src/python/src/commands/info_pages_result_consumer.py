from sqlalchemy.dialects.mysql import insert
from scrapy.utils.project import get_project_settings

from database.models.info_page import InfoPage
from rmq.commands import Consumer


class InfoPagesResultConsumer(Consumer):
    def init_queue_name(self, opts):
        self.project_settings = get_project_settings()
        self.queue_name = queue_name = self.project_settings.get("RABBITMQ_INFO_RESULTS")
        return queue_name

    def build_message_store_stmt(self, message_body):
        stmt = insert(InfoPage)
        stmt = stmt.prefix_with('IGNORE')
        stmt = stmt.values({
            "business_id": message_body['business_id'],
            "business_name": message_body['business_name'],
            "business_address": message_body['business_address'],
            "business_category": message_body['business_category'],
            "business_web_url": message_body['business_web_url'],
            "business_img_url": message_body['business_img_url'],
            "business_detailed_url": message_body['business_detailed_url'],
            "business_phone": message_body['business_phone'],
            "business_fax": message_body['business_fax'],
            "business_hours": message_body['business_hours'],
            "business_stars": message_body['business_stars'],
            "business_customer_reviews": message_body['business_customer_reviews'],
            "business_bbb_rating": message_body['business_bbb_rating'],
            "business_accredited_date": message_body['business_accredited_date'],
            "business_social_media": message_body['business_social_media'],
            "business_years": message_body['business_years'],
            "business_started_date": message_body['business_started_date'],
            "parse_date": message_body['parse_date'],
            "business_contact_information": message_body['business_contact_information'],
            "business_management": message_body['business_management']
        })
        return stmt
