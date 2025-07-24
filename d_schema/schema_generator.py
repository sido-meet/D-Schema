# d_schema/schema_generator.py

from .structures import DatabaseSchema

class SchemaGenerator:
    """
    Generates different schema formats from a DatabaseSchema object.
    """
    def __init__(self, schema: DatabaseSchema):
        """
        Initializes the generator with a DatabaseSchema object.

        Args:
            schema: A DatabaseSchema object containing the database structure.
        """
        self.schema = schema

    def generate_ddl_schema(self) -> str:
        """
        Generates a DDL schema (CREATE TABLE statements).

        Returns:
            A string containing the DDL schema.
        """
        schema_parts = []
        for table in self.schema.tables:
            schema_parts.append(f"# Table: {table.name}")
            statement_parts = [f"CREATE TABLE {table.name} ("]
            
            column_defs = []
            primary_keys = []
            foreign_keys = []

            for column in table.columns:
                col_def = f"    {column.name} {column.type}"
                if not column.nullable:
                    col_def += " NOT NULL"
                column_defs.append(col_def)

                if column.primary_key:
                    primary_keys.append(column.name)
                if column.foreign_key:
                    foreign_keys.append(f"    FOREIGN KEY ({column.name}) {column.foreign_key}")
            
            statement_parts.append(",\n".join(column_defs))

            if primary_keys:
                statement_parts.append(f",\n    PRIMARY KEY ({', '.join(primary_keys)})")
            
            if foreign_keys:
                statement_parts.append(",\n" + ",\n".join(foreign_keys))

            statement_parts.append("\n);");
            schema_parts.append("\n".join(statement_parts))
            schema_parts.append("")  # Add a blank line for readability
        
        return "\n".join(schema_parts)

    def generate_mac_sql_schema(self) -> str:
        """
        Generates a MAC-SQL schema.

        Returns:
            A string containing the MAC-SQL schema.
        """
        schema_parts = []
        for table in self.schema.tables:
            schema_parts.append(f"# Table: {table.name}")
            schema_parts.append("[")
            
            column_details = []
            for column in table.columns:
                comment = column.comment or f"the {column.name.replace('_', ' ')} of the {table.name}"
                samples_str = ", ".join([f"'{s}'" for s in column.samples])
                column_details.append(f"({column.name}, {comment}. Value examples: [{samples_str}].)")
            
            schema_parts.append("\n".join(column_details))
            schema_parts.append("]")
            schema_parts.append("")  # Add a blank line for readability
        
        return "\n".join(schema_parts)

