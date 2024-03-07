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
            "bbb_id": message_body['bbb_id'],
            "name": message_body['name'],
            "address": message_body['address'],
            "category": message_body['category'],
            "web_url": message_body['web_url'],
            "img_url": message_body['img_url'],
            "detailed_url": message_body['detailed_url'],
            "phone": message_body['phone'],
            "fax": message_body['fax'],
            "hours": message_body['hours'],
            "stars": message_body['stars'],
            "customer_reviews": message_body['customer_reviews'],
            "bbb_rating": message_body['bbb_rating'],
            "accredited_date": message_body['accredited_date'],
            "social_media": message_body['social_media'],
            "years": message_body['years'],
            "started_date": message_body['started_date'],
            "parse_date": message_body['parse_date'],
            "contact_information": message_body['contact_information'],
            "management": message_body['management']
        })
        return stmt
