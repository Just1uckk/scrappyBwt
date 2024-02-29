from datetime import datetime
from typing import Dict

from sqlalchemy import update

from commands.base import BaseCSVExporter
from database.models.info_page import InfoPage
from sqlalchemy.sql.base import Executable as SQLAlchemyExecutable


class BusinessExporterCommand(BaseCSVExporter):
    table = InfoPage

    def build_update_query_stmt(self, row: Dict) -> SQLAlchemyExecutable:
        export_date = {self.export_date_column: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}
        update_date_stmt = update(self.table).values(**export_date)
        return update_date_stmt.where(self.table.id == row['id'])
