from typing import List, Dict, Any

from d_schema.structures import TableInfo, ColumnInfo
from d_schema.generators.base_generator import BaseGenerator


class MacSQLSchemaGenerator(BaseGenerator):
    """
    Generates a MAC-SQL schema, including profiling data if available.
    """

    def generate_column(self, column: ColumnInfo, table_name: str, table_record_count: int) -> str:
        """
        Generates the MAC-SQL representation for a single column.
        """
        comment = column.comment or f"the {column.name.replace('_', ' ')} of the {table_name}"
        samples_str = ", ".join([f"'{s}'" for s in column.samples])
        base_detail = f"({column.name}, {comment}. Value examples: [{samples_str}].)"

        if column.profile:
            profile_parts = []
            if column.profile.non_null_count is not None and table_record_count > 0:
                non_null_pct = (column.profile.non_null_count / table_record_count) * 100
                profile_parts.append(f"{non_null_pct:.1f}% non-null")
            if column.profile.distinct_count is not None:
                profile_parts.append(f"{column.profile.distinct_count} distinct")
            if column.profile.min_value is not None:
                profile_parts.append(f"min='{column.profile.min_value}'")
            if column.profile.max_value is not None:
                profile_parts.append(f"max='{column.profile.max_value}'")
            if column.profile.avg_char_length is not None:
                profile_parts.append(f"avg_len={column.profile.avg_char_length:.1f}")
            
            if profile_parts:
                base_detail += f" (Profile: {', '.join(profile_parts)})"

        return base_detail

    def generate_table(self, table: TableInfo) -> str:
        """
        Generates the MAC-SQL schema representation for a single table.
        """
        table_header = f"# Table: {table.name}"
        record_count = 0
        if table.profile and table.profile.record_count is not None:
            record_count = table.profile.record_count
            table_header += f" ({record_count} rows)"
        
        column_details = [self.generate_column(col, table.name, record_count) for col in table.columns]
        
        return f"{table_header}\n[\n" + "\n".join(column_details) + "\n]"

    def generate_schema(self) -> str:
        """
        Assembles the final MAC-SQL schema for all tables into a single string.
        """
        # The base implementation needs to be adjusted because generate_column needs table-level info
        # and generate_table produces the final formatted block for a table.
        return "\n\n".join([self.generate_table(table) for table in self.tables])