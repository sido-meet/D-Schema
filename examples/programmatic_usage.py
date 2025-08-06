# examples/programmatic_usage.py

import os
from d_schema import (
    DatabaseParser,
    DDLSchemaGenerator,
    MSchemaGenerator,
    ProfileReportGenerator,
)

# --- Configuration ---
# Build a robust path to the database file relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "..", "test_data", "test.db")
DB_URL = f"sqlite:///{DB_PATH}"

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "programmatic_output")


def main():
    """
    Demonstrates how to use the d-schema library programmatically.
    """
    print(f"Connecting to database: {DB_URL}")
    
    # 1. Initialize the parser and parse the database structure
    # Set profile=True if you need data for generators like ProfileReportGenerator
    # Set num_samples to control how many distinct values are fetched.
    parser = DatabaseParser(db_url=DB_URL)
    db_structure = parser.parse(profile=True, num_samples=1)
    print(f"{db_structure.db_name} database parsed successfully.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output will be saved to: {OUTPUT_DIR}")

    # 2. Initialize and run the desired generators

    # --- DDL Schema Example ---
    print("\nRunning DDLSchemaGenerator...")
    # The number of examples shown is now controlled by the parser's num_samples
    ddl_generator = DDLSchemaGenerator(
        schema=db_structure,
        allow_comments=True,
        include_comment_text=True,
        include_examples=True,
        include_profiling=True,
    )
    ddl_content = ddl_generator.generate_schema()
    ddl_filepath = os.path.join(OUTPUT_DIR, "schema.ddl")
    with open(ddl_filepath, "w", encoding="utf-8") as f:
        f.write(ddl_content)
    print(f"DDL schema written to {ddl_filepath}")

    # --- Profile Report Example ---
    print("\nRunning ProfileReportGenerator...")
    profile_generator = ProfileReportGenerator(schema=db_structure)
    profile_content = profile_generator.generate_schema()
    profile_filepath = os.path.join(OUTPUT_DIR, "profile_report.md")
    with open(profile_filepath, "w", encoding="utf-8") as f:
        f.write(profile_content)
    print(f"Profile report written to {profile_filepath}")


if __name__ == "__main__":
    main()
