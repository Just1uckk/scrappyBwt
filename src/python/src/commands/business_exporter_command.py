from commands.base import BaseCSVExporter
from database.models.info_page import InfoPage


class BusinessExporterCommand(BaseCSVExporter):
    table = InfoPage
