# d_schema/main.py

import argparse
from d_schema.db_parser import DatabaseParser
from d_schema.schema_generator import SchemaGenerator

def main():
    """
    Command-line interface for D-Schema.
    """
    parser = argparse.ArgumentParser(description="Generate database schemas in various formats.")
    parser.add_argument("--db-url", required=True, help="The SQLAlchemy database URL (e.g., 'sqlite:///mydatabase.db')")
    parser.add_argument("--schema-type", required=True, choices=['ddl', 'mac-sql', 'm-schema'], default='ddl', help="The type of schema to generate.")
    
    args = parser.parse_args()
    
    try:
        # 1. Parse the database
        print(f"Connecting to {args.db_url}...")
        db_parser = DatabaseParser(db_url=args.db_url)
        database_schema = db_parser.parse()
        print("Database parsed successfully.")

        # 2. Generate the schema
        schema_generator = SchemaGenerator(schema=database_schema)
        
        output_schema = ""
        if args.schema_type == 'ddl':
            print("Generating DDL schema...")
            output_schema = schema_generator.generate_ddl_schema()
        elif args.schema_type == 'mac-sql':
            print("Generating MAC-SQL schema...")
            output_schema = schema_generator.generate_mac_sql_schema()
        elif args.schema_type == 'm-schema':
            print("Generating M-Schema...")
            output_schema = schema_generator.generate_m_schema()
        else:
            print(f"Schema type '{args.schema_type}' is not yet supported.")
            return

        # 3. Print the result
        print("\n--- Generated Schema ---\n")
        print(output_schema)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
