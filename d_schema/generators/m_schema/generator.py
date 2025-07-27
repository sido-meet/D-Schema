from typing import List, Dict, Any

from d_schema.structures import TableInfo, ColumnInfo, DatabaseSchema
from d_schema.generators.base_generator import BaseGenerator


class MSchemaGenerator(BaseGenerator):
    """
    Generates a M-Schema representation of the database.
    """

    def __init__(self, schema: DatabaseSchema):
        """
        Initializes the generator with a DatabaseSchema object.
        M-Schema requires the db_name, so we override the init.
        """
        super().__init__(schema.tables)
        self.db_name = schema.db_name

    def generate_column(self, column: ColumnInfo, table_name: str) -> str:
        """
        Generates the M-Schema representation for a single column.
        """
        col_parts = [f"{column.name}:{column.type}"]
        if column.primary_key:
            col_parts.append("Primary Key")
        
        comment = column.comment or f"the {column.name.replace('_', ' ')} of the {table_name}"
        col_parts.append(comment)

        if column.foreign_key:
            fk_target = column.foreign_key.replace('REFERENCES ', '')
            col_parts.append(f"Maps to {fk_target}")

        if column.samples:
            samples_str = ", ".join([f"{s}" for s in column.samples])
            col_parts.append(f"Examples:[{samples_str}]")

        if column.profile:
            profile_parts = []
            if column.profile.non_null_count is not None and column.profile.null_count is not None:
                total = column.profile.non_null_count + column.profile.null_count
                if total > 0:
                    non_null_pct = (column.profile.non_null_count / total) * 100
                    profile_parts.append(f"{non_null_pct:.1f}% non-null")
            if column.profile.distinct_count is not None:
                profile_parts.append(f"{column.profile.distinct_count} distinct values")
            if profile_parts:
                col_parts.append(f"Profile: {', '.join(profile_parts)}")
        
        return f"({', '.join(col_parts)})"

    def generate_table(self, table: TableInfo) -> str:
        """
        Generates the M-Schema representation for a single table, including its columns.
        """
        header = f"# Table: {table.name}"
        column_defs = [self.generate_column(col, table.name) for col in table.columns]
        return "\n".join([header] + column_defs)

    def generate_schema(self) -> str:
        """
        Assembles the final M-Schema for all tables into a single string.
        """
        # 1. DB_ID and Schema Header
        schema_parts = [f"[DB_ID] {self.db_name}\n", "[Schema]"]

        # 2. Generate each table's schema
        foreign_keys_list = []
        for table in self.tables:
            schema_parts.append(self.generate_table(table))
            schema_parts.append("")  # Blank line for readability

            # 3. Collect all foreign keys for the final section
            for column in table.columns:
                if column.foreign_key:
                    fk_target = column.foreign_key.replace('REFERENCES ', '')
                    fk_table_name = table.name
                    fk_col_name = column.name
                    ref_table, ref_col = fk_target.split('(')
                    ref_col = ref_col[:-1]
                    foreign_keys_list.append(f"{fk_table_name}.{fk_col_name} = {ref_table}.{ref_col}")

        # 4. Append the foreign keys section if needed
        if foreign_keys_list:
            schema_parts.append("[Foreign keys]")
            schema_parts.extend(foreign_keys_list)

        return "\n".join(schema_parts)