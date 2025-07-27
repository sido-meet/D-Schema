from typing import List, Dict, Any

from d_schema.structures import TableInfo, ColumnInfo
from d_schema.generators.base_generator import BaseGenerator


class DDLSchemaGenerator(BaseGenerator):
    """
    Generates a DDL schema (CREATE TABLE statements) using a bottom-up approach.
    """

    def generate_column(self, column: ColumnInfo) -> str:
        """
        Generates the DDL definition for a single column.
        Example: 'id INTEGER NOT NULL -- Profile: 100.0% non-null, 1500 distinct'
        """
        col_def = f"    {column.name} {column.type}"
        if not column.nullable:
            col_def += " NOT NULL"
        
        if column.profile:
            profile_parts = []
            if column.profile.non_null_count is not None and column.profile.null_count is not None:
                total = column.profile.non_null_count + column.profile.null_count
                if total > 0:
                    non_null_pct = (column.profile.non_null_count / total) * 100
                    profile_parts.append(f"{non_null_pct:.1f}% non-null")
            if column.profile.distinct_count is not None:
                profile_parts.append(f"{column.profile.distinct_count} distinct")
            
            if profile_parts:
                col_def += f"  -- Profile: {', '.join(profile_parts)}"

        return col_def

    def generate_table(self, table: TableInfo) -> str:
        """
        Generates a full CREATE TABLE statement for a single table.
        """
        statement_parts = [f"CREATE TABLE {table.name} ("]
        
        column_defs = [self.generate_column(col) for col in table.columns]
        primary_keys = [col.name for col in table.columns if col.primary_key]
        foreign_keys = [
            f"    FOREIGN KEY ({col.name}) {col.foreign_key}" 
            for col in table.columns if col.foreign_key
        ]

        all_parts = column_defs
        if primary_keys:
            all_parts.append(f"    PRIMARY KEY ({', '.join(primary_keys)})")
        if foreign_keys:
            all_parts.extend(foreign_keys)

        statement_parts.append(",\n".join(all_parts))
        statement_parts.append("\n);");
        return "\n".join(statement_parts)

    def generate_schema(self) -> str:
        """
        Assembles the final DDL schema for all tables into a single string.
        """
        schema_parts = []
        for table in self.tables:
            schema_parts.append(f"# Table: {table.name}")
            schema_parts.append(self.generate_table(table))
            schema_parts.append("")  # Add a blank line for readability
        
        return "\n".join(schema_parts)
