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
        Generates a MAC-SQL schema, including profiling data if available.

        Returns:
            A string containing the MAC-SQL schema.
        """
        schema_parts = []
        for table in self.schema.tables:
            table_header = f"# Table: {table.name}"
            if table.profile and table.profile.record_count is not None:
                table_header += f" ({table.profile.record_count} rows)"
            schema_parts.append(table_header)
            schema_parts.append("[")
            
            column_details = []
            for column in table.columns:
                comment = column.comment or f"the {column.name.replace('_', ' ')} of the {table.name}"
                samples_str = ", ".join([f"'{s}'" for s in column.samples])
                base_detail = f"({column.name}, {comment}. Value examples: [{samples_str}].)"

                # Append profiling information if available
                if column.profile:
                    profile_parts = []
                    if column.profile.non_null_count is not None and table.profile.record_count > 0:
                        non_null_pct = (column.profile.non_null_count / table.profile.record_count) * 100
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
                        base_detail += f" (Profile: { ', '.join(profile_parts) })"

                column_details.append(base_detail)
            
            schema_parts.append("\n".join(column_details))
            schema_parts.append("]")
            schema_parts.append("")  # Add a blank line for readability
        
        return "\n".join(schema_parts)

    def generate_m_schema(self) -> str:
        """
        Generates a M-Schema representation of the database.

        Returns:
            A string containing the M-Schema representation.
        """
        schema_parts = [f"[DB_ID] {self.schema.db_name}\n"]
        schema_parts.append("[Schema]")

        foreign_keys_list = []

        for table in self.schema.tables:
            schema_parts.append(f"# Table: {table.name}")
            
            for column in table.columns:
                col_parts = [f"{column.name}:{column.type}"]
                if column.primary_key:
                    col_parts.append("Primary Key")
                
                comment = column.comment or f"the {column.name.replace('_', ' ')} of the {table.name}"
                col_parts.append(comment)

                if column.foreign_key:
                    fk_target = column.foreign_key.replace('REFERENCES ', '')
                    col_parts.append(f"Maps to {fk_target}")
                    
                    # Extract foreign key details for the [Foreign keys] section
                    fk_table_name = table.name
                    fk_col_name = column.name
                    ref_table, ref_col = fk_target.split('(')
                    ref_col = ref_col[:-1] # Remove closing parenthesis
                    foreign_keys_list.append(f"{fk_table_name}.{fk_col_name} = {ref_table}.{ref_col}")

                if column.samples:
                    samples_str = ", ".join([f"{s}" for s in column.samples])
                    col_parts.append(f"Examples:[{samples_str}]")
                
                schema_parts.append(f"({', '.join(col_parts)})")
            schema_parts.append("") # Add a blank line for readability

        if foreign_keys_list:
            schema_parts.append("[Foreign keys]")
            schema_parts.extend(foreign_keys_list)

        return "\n".join(schema_parts)

