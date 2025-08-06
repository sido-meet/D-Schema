from typing import List, Dict, Any

from d_schema.structures import TableInfo, ColumnInfo, DatabaseSchema
from d_schema.generators.base_generator import BaseGenerator


class DDLSchemaGenerator(BaseGenerator):
    """
    Generates a DDL schema (CREATE TABLE statements) with configurable comments.
    """

    def __init__(
        self,
        schema: DatabaseSchema,
        allow_comments: bool = True,
        include_comment_text: bool = True,
        include_examples: bool = True,
        include_profiling: bool = True,
    ):
        """
        Initializes the DDL generator with schema and comment configurations.
        """
        super().__init__(schema)
        self.allow_comments = allow_comments
        self.include_comment_text = include_comment_text
        self.include_examples = include_examples
        self.include_profiling = include_profiling

    def generate_column(self, column: ColumnInfo) -> str:
        """
        Generates the DDL definition for a single column, including
        configurable comments.
        """
        col_def = f"    {column.name} {column.type}"
        if not column.nullable:
            col_def += " NOT NULL"

        if not self.allow_comments:
            return col_def

        comment_parts = []

        # 1. Add the column's own comment text
        if self.include_comment_text and column.comment:
            comment_parts.append(column.comment)

        # 2. Add data examples
        if self.include_examples and column.samples:
            samples_str = ", ".join(map(str, column.samples))
            comment_parts.append(f"example: [{samples_str}]")

        # 3. Add profiling information
        if self.include_profiling and column.profile:
            profile_parts = []
            if column.profile.non_null_count is not None and column.profile.null_count is not None:
                total = column.profile.non_null_count + column.profile.null_count
                if total > 0:
                    non_null_pct = (column.profile.non_null_count / total) * 100
                    profile_parts.append(f"{non_null_pct:.1f}% non-null")
            if column.profile.distinct_count is not None:
                profile_parts.append(f"{column.profile.distinct_count} distinct")
            
            if profile_parts:
                comment_parts.append(f"Profile: {', '.join(profile_parts)}")

        # Assemble the final comment string only if there are parts to join
        if comment_parts:
            col_def += f"  -- {'; '.join(comment_parts)}"

        return col_def

    def generate_table(self, table: TableInfo) -> str:
        """
        Generates a full CREATE TABLE statement for a single table.
        """
        statement_parts = [f"CREATE TABLE {table.name} ("]
        
        definitions = []
        definitions.extend([self.generate_column(col) for col in table.columns])
        
        primary_keys = [col.name for col in table.columns if col.primary_key]
        if primary_keys:
            definitions.append(f"    PRIMARY KEY ({', '.join(primary_keys)})")

        foreign_keys = [
            f"    FOREIGN KEY ({col.name}) {col.foreign_key}" 
            for col in table.columns if col.foreign_key
        ]
        definitions.extend(foreign_keys)

        statement_parts.append(",\n".join(definitions))
        statement_parts.append(");")
        
        return "\n".join(statement_parts)

    def generate_schema(self) -> str:
        """
        Assembles the final DDL schema for all tables into a single string.
        """
        schema_parts = [self.generate_table(table) for table in self.tables]
        
        return "\n\n".join(schema_parts)
