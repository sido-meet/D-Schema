from d_schema.structures import TableInfo, ColumnInfo
from d_schema.generators.base_generator import BaseGenerator


class ProfileReportGenerator(BaseGenerator):
    """
    Generates a detailed data profiling report in Markdown format.
    """

    def generate_column(self, column: ColumnInfo) -> str:
        """
        Generates the Markdown table row for a single column's profile.
        """
        if not column.profile:
            return f"| {column.name} | {column.type} | *No profile data* |"

        p = column.profile
        total = (p.non_null_count or 0) + (p.null_count or 0)
        non_null_pct = f"{(p.non_null_count / total) * 100:.1f}%" if total > 0 else "N/A"
        distinct_count = str(p.distinct_count) if p.distinct_count is not None else "N/A"
        
        top_k_str = ""
        if p.top_k_values:
            top_k_str = ", ".join([f"'{val}' ({count})" for val, count in p.top_k_values])

        details = (
            f"**Non-Null**: {non_null_pct}<br>"
            f"**Distinct**: {distinct_count}<br>"
            f"**Min**: {p.min_value or 'N/A'}<br>"
            f"**Max**: {p.max_value or 'N/A'}<br>"
            f"**Avg. Len**: {p.avg_char_length:.2f}" if p.avg_char_length is not None else ""
        )

        if top_k_str:
            details += f"<br>**Top Values**: {top_k_str}"

        return f"| {column.name} | {column.type} | {details} |"

    def generate_table(self, table: TableInfo) -> str:
        """
        Generates the Markdown section for a single table.
        """
        record_count = "N/A"
        if table.profile and table.profile.record_count is not None:
            record_count = str(table.profile.record_count)

        header = f"### Table: `{table.name}`\n*Record Count: {record_count}*\n"
        
        table_md = [
            header,
            "| Column Name | Data Type | Profile Details |",
            "|-------------|-----------|-----------------|"
        ]
        
        for col in table.columns:
            table_md.append(self.generate_column(col))
        
        return "\n".join(table_md)

    def generate_schema(self) -> str:
        """
        Assembles the final Markdown report for all tables.
        """
        report_parts = ["# Data Profiling Report\n"]
        
        for table in self.tables:
            report_parts.append(self.generate_table(table))
            report_parts.append("\n---\n")

        return "\n".join(report_parts)
