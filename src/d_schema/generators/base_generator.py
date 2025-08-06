from abc import ABC, abstractmethod
from typing import List, Dict, Any

from d_schema.structures import TableInfo, ColumnInfo, DatabaseSchema


class BaseGenerator(ABC):
    """
    Abstract base class for all schema generators.

    It defines a standard interface for generating schemas from a DatabaseSchema
    object. Subclasses must implement the specific logic for generating parts
    of the schema (e.g., for a column or a table).
    """

    def __init__(self, schema: DatabaseSchema):
        self.schema = schema
        self.tables = schema.tables

    @abstractmethod
    def generate_column(self, column: ColumnInfo) -> Dict[str, Any]:
        """
        Generates the schema definition for a single column.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def generate_table(self, table: TableInfo) -> Dict[str, Any]:
        """
        Generates the schema definition for a single table.
        Must be implemented by subclasses.
        """
        pass

    def generate_schema(self) -> str:
        """
        Assembles the final schema for all tables into a single string.

        This method iterates through the tables, calls generate_table for each,
        and combines them. Subclasses can override this to customize the
        final assembly and formatting (e.g., wrapping in a specific JSON
        structure).
        """
        all_schemas = {
            table.name: self.generate_table(table)
            for table in self.tables
        }
        
        # Default to a simple JSON representation.
        # Subclasses should override this to provide specific formatting
        # like DDL, Avro, or custom M-Schema.
        import json
        return json.dumps(all_schemas, indent=2)
