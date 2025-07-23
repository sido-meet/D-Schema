
from sqlalchemy import MetaData
from sqlalchemy.schema import CreateTable

class SchemaGenerator:
    """
    Generates different schema formats from SQLAlchemy metadata.
    """
    def __init__(self, metadata: MetaData):
        """
        Initializes the generator with database metadata.

        Args:
            metadata: A SQLAlchemy MetaData object.
        """
        self.metadata = metadata

    def generate_ddl_schema(self, engine) -> str:
        """
        Generates a DDL schema (CREATE TABLE statements).

        Args:
            engine: The SQLAlchemy engine instance.

        Returns:
            A string containing the DDL schema.
        """
        schema_parts = []
        for table in self.metadata.tables.values():
            # Add a comment for the table name
            schema_parts.append(f"# Table: {table.name}")
            # Generate the CREATE TABLE statement
            statement = str(CreateTable(table).compile(dialect=engine.dialect)).strip()

            schema_parts.append(statement + ";")
            schema_parts.append("") # Add a blank line for readability
        
        return "\n".join(schema_parts)
