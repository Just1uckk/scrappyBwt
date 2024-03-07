from datetime import datetime
from typing import Dict, List

from sqlalchemy import update

from commands.base import BaseCSVExporter
from database.models.business_model import BusinessModel
from sqlalchemy.sql.base import Executable as SQLAlchemyExecutable


class BusinessExporterCommand(BaseCSVExporter):
    table = BusinessModel
    excluded_columns: List[str] = ['sent_to_customer', 'created_at', 'updated_at']

    def build_update_query_stmt(self, row: Dict) -> SQLAlchemyExecutable:
        export_date = {self.export_date_column: datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S.%fZ')}
        update_date_stmt = update(self.table).values(**export_date)
        return update_date_stmt.where(self.table.id == row['id'])
