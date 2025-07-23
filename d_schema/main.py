
import argparse
from d_schema.db_parser import DatabaseParser
from d_schema.schema_generator import SchemaGenerator

def main():
    """
    Command-line interface for D-Schema.
    """
    parser = argparse.ArgumentParser(description="Generate database schemas in various formats.")
    parser.add_argument("--db-url", required=True, help="The SQLAlchemy database URL (e.g., 'sqlite:///mydatabase.db')")
    parser.add_argument("--schema-type", required=True, choices=['ddl'], default='ddl', help="The type of schema to generate.")
    
    args = parser.parse_args()
    
    try:
        # 1. Parse the database
        print(f"Connecting to {args.db_url}...")
        db_parser = DatabaseParser(db_url=args.db_url)
        metadata = db_parser.get_metadata()
        print("Database parsed successfully.")

        # 2. Generate the schema
        schema_generator = SchemaGenerator(metadata=metadata)
        
        output_schema = ""
        if args.schema_type == 'ddl':
            print("Generating DDL schema...")
            output_schema = schema_generator.generate_ddl_schema(engine=db_parser.engine)
        else:
            # This part will be expanded for other schema types
            print(f"Schema type '{args.schema_type}' is not yet supported.")
            return

        # 3. Print the result
        print("\n---" + " Generated Schema ---\n")
        print(output_schema)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
