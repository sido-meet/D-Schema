import d_schema
import os

# 1. Define your database connection URL
# Using the test database provided in the project
DB_URL = "sqlite:///./test_data/test.db"

# 2. Define where to save the output files
OUTPUT_DIR = "./schema_output"

# 3. Specify which generators you want to run
GENERATORS_TO_RUN = ["ddl", "m_schema", "mac_sql", "profile_report"]

# 4. Run the generation process
print(f"Starting schema generation for database: {DB_URL}")
try:
    d_schema.generate(
        db_url=DB_URL,
        output_path=OUTPUT_DIR,
        generators=GENERATORS_TO_RUN
    )
    print(f"\nSchema files successfully generated in '{OUTPUT_DIR}'")
    print("\nGenerated files:")
    for filename in os.listdir(OUTPUT_DIR):
        print(f"- {filename}")

except Exception as e:
    print(f"An error occurred: {e}")
