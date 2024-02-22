from sqlalchemy.dialects.mysql import insert

from database.models.info_page import InfoPage
from rmq.commands import Consumer


class InfoPagesResultConsumer(Consumer):
    def init_queue_name(self, opts):
        self.queue_name = queue_name = 'info_spider_result_queue'
        return queue_name

    def build_message_store_stmt(self, message_body):
        stmt = insert(InfoPage)
        stmt = stmt.on_duplicate_key_update({
            'status': stmt.inserted.status
        }).values({
            "status": message_body['status'],
            "exception": message_body['exception'],
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
