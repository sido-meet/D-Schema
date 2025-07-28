## Testing

This project is tested against multiple relational databases to ensure its general applicability. We use Docker to run instances of PostgreSQL and MySQL for testing without requiring local installation.

### 1. Start Database Services

Make sure you have Docker installed and running. Then, start the required database containers:

- **PostgreSQL:**
  ```bash
  docker run --name test-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
  ```
  For subsequent runs, if the container is stopped, use: `sudo docker start test-postgres`
- **MySQL:**
  ```bash
  docker run --name test-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -p 3306:3306 -d mysql
  ```
  For subsequent runs, if the container is stopped, use: `sudo docker start test-mysql`

### 2. Set Up Test Databases

A helper script is provided to create the necessary databases and tables for testing.

Run the setup script:
```bash
uv run python setup_dbs.py
```
This will:
- Create a `test.db` SQLite file in the `test_data` directory.
- Create a `test_schema` database in MySQL and populate it.
- Create the necessary tables in the `public` schema in PostgreSQL.

### 3. Run the Verification Script

A convenience script, `run_tests.sh`, is provided to execute `d-schema` against all three configured databases.

```bash
bash run_tests.sh
```
This will run the DDL and MAC-SQL generation for SQLite, PostgreSQL, and MySQL, allowing you to verify the output for each.
