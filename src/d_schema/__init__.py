"""
D-Schema: Database Schema Generation and Analysis Toolkit

This module provides the primary entry point for generating various schema
representations from a database connection.
"""
import os
from .db_parser import DatabaseParser
from .structures import DatabaseSchema
from .generators.ddl_schema.generator import DDLSchemaGenerator
from .generators.m_schema.generator import MSchemaGenerator
from .generators.mac_sql_schema.generator import MacSQLSchemaGenerator
from .generators.profile_report.generator import ProfileReportGenerator


# A mapping from generator names to their classes and output filenames
AVAILABLE_GENERATORS = {
    "ddl": (DDLSchemaGenerator, "schema.ddl"),
    "m_schema": (MSchemaGenerator, "schema.mschema"),
    "mac_sql": (MacSQLSchemaGenerator, "schema.macsql"),
    "profile_report": (ProfileReportGenerator, "profile_report.md"),
}

__all__ = ["generate", "DatabaseSchema", "AVAILABLE_GENERATORS"]
__version__ = "0.1.0"

def generate(db_url: str, output_path: str, generators: list[str]) -> None:
    """
    Connects to a database, parses its structure, and runs the specified
    generators to create schema files.

    Args:
        db_url (str): The database connection URL (e.g., 
                      "postgresql://user:pass@host:port/dbname").
        output_path (str): The directory where generated files will be saved.
        generators (list[str]): A list of generator names to run.
                                Available options are in AVAILABLE_GENERATORS.
    """
    # Determine if detailed (and slower) profiling is needed
    should_profile = "profile_report" in generators
    
    print("Initializing database parser...")
    parser = DatabaseParser(db_url)
    
    print(f"Parsing database structure... (Profiling enabled: {should_profile})")
    db_structure: DatabaseSchema = parser.parse(profile=should_profile)
    print("Database parsed successfully.")

    os.makedirs(output_path, exist_ok=True)

    for gen_name in generators:
        if gen_name not in AVAILABLE_GENERATORS:
            print(f"Warning: Generator '{gen_name}' not found. Skipping.")
            continue

        print(f"Running generator: {gen_name}...")
        generator_class, output_filename = AVAILABLE_GENERATORS[gen_name]
        
        generator_instance = generator_class(db_structure)
        
        schema_content = generator_instance.generate_schema()
        
        file_path = os.path.join(output_path, output_filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(schema_content)
            
        print(f"Generator {gen_name} finished. Output written to {file_path}")