# d_schema/main.py

import argparse
import importlib
import pkgutil
from typing import Dict, Type

from d_schema.db_parser import DatabaseParser
from d_schema.generators.base_generator import BaseGenerator
import d_schema.generators

def load_generators() -> Dict[str, Type[BaseGenerator]]:
    """
    Dynamically loads all generator plugins from the d_schema.generators package.
    """
    generators = {}
    package = d_schema.generators
    for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
        if is_pkg:
            try:
                module = importlib.import_module(f'{package.__name__}.{name}.generator')
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, BaseGenerator) and attribute is not BaseGenerator:
                        # The key is the package name, e.g., 'ddl_schema'
                        generators[name.replace('_', '-')] = attribute
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Could not load generator from '{name}': {e}")
    return generators

def main():
    """
    Command-line interface for D-Schema.
    """
    available_generators = load_generators()
    
    parser = argparse.ArgumentParser(description="Generate database schemas in various formats.")
    parser.add_argument("--db-url", required=True, help="The SQLAlchemy database URL (e.g., 'sqlite:///mydatabase.db')")
    parser.add_argument("--schema-type", required=True, choices=list(available_generators.keys()), help="The type of schema to generate.")
    parser.add_argument("--profile", action='store_true', help="Enable detailed data profiling (can be slow).")

    args = parser.parse_args()
    
    try:
        # 1. Parse the database
        print(f"Connecting to {args.db_url}...")
        db_parser = DatabaseParser(db_url=args.db_url)
        database_schema = db_parser.parse(profile=args.profile)
        print("Database parsed successfully.")

        # 2. Get the selected generator class
        GeneratorClass = available_generators.get(args.schema_type)
        if not GeneratorClass:
            print(f"Schema type '{args.schema_type}' is not supported.")
            return

        # 3. Instantiate and run the generator
        print(f"Generating {args.schema_type} schema...")
        
        # Handle the special case for MSchemaGenerator which needs the whole schema object
        if args.schema_type == 'm-schema':
            generator_instance = GeneratorClass(schema=database_schema)
        else:
            generator_instance = GeneratorClass(tables=database_schema.tables)
            
        output_schema = generator_instance.generate_schema()

        # 4. Print the result
        print("\n--- Generated Schema ---\n")
        print(output_schema)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
