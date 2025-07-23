
# This script runs the d-schema tool against all configured test databases
# to verify the DDL schema generation.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- VERIFYING SQLITE ---"
uv run d-schema --db-url "sqlite:///test_data/test.db" --schema-type ddl
echo ""
echo "--- SQLite verification complete. ---"
echo ""

echo "--- VERIFYING POSTGRESQL ---"
uv run d-schema --db-url "postgresql://postgres:mysecretpassword@localhost:5432/postgres" --schema-type ddl
echo ""
echo "--- PostgreSQL verification complete. ---"
echo ""

echo "--- VERIFYING MYSQL ---"
uv run d-schema --db-url "mysql+mysqlconnector://root:mysecretpassword@localhost:3306/test_schema" --schema-type ddl
echo ""
echo "--- MySQL verification complete. ---"
echo ""

echo "All tests completed successfully!"
