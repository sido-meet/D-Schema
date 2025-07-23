# D-Schema

D-Schema is a versatile Python-based tool designed to connect to a given database, parse its structure, and generate various database schema definitions. The core of the project utilizes SQLAlchemy to create an in-memory representation of the database, which is then used to build different schema formats. This flexible architecture allows for easy extension to support new schema types in the future.

## Features

- **Dynamic Database Parsing**: Leverages `SQLAlchemy` to support a wide range of database backends (including SQLite, PostgreSQL, MySQL, etc.).
- **Multiple Schema Formats**: Designed to generate various types of schema definitions from a single database source.
  - **Currently Implemented**:
    - `DDL Schema`: The standard `CREATE TABLE` SQL statements.
  - **Planned**:
    - `MAC-SQL Schema`: A detailed, commented format suitable for analysis.
    - `M-Schema`: A compact, human-readable format.
- **Extensible by Design**: The internal class structure makes it straightforward to add new schema generators.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/D-Schema.git
    cd D-Schema
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    The project uses `pyproject.toml` and `uv` for dependency management.
    ```bash
    uv pip install -e .
    ```

## Usage

To generate a schema, use the `d-schema` command-line tool.

**Example:**
```bash
d-schema --db-url "sqlite:///test_data/test.db" --schema-type ddl
```

- `--db-url`: The SQLAlchemy database URL for the target database.
- `--schema-type`: The type of schema to generate. Currently, only `ddl` is supported.

## Testing

This project is tested against multiple relational databases to ensure its general applicability. We use Docker to run instances of PostgreSQL and MySQL for testing without requiring local installation.

### 1. Start Database Services

Make sure you have Docker installed and running. Then, start the required database containers:

- **PostgreSQL:**
  ```bash
  docker run --name test-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
  ```
- **MySQL:**
  ```bash
  docker run --name test-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -p 3306:3306 -d mysql
  ```

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
This will run the DDL generation for SQLite, PostgreSQL, and MySQL, allowing you to verify the output for each.

## Schema Formats Explained

This section provides examples of the different schema formats that D-Schema aims to support, using a sample `superhero` database.

### 1. DDL Schema

Standard SQL Data Definition Language (DDL) statements. This format is ideal for recreating the database structure.

**Example (`superhero` database):**
```sql
# Table: hero_power
CREATE TABLE hero_power (
    hero_id INTEGER,
    power_id INTEGER,
    FOREIGN KEY (hero_id) REFERENCES hero(id),
    FOREIGN KEY (power_id) REFERENCES superpower(id)
);

# Table: superpower
CREATE TABLE superpower (
    id INTEGER PRIMARY KEY,
    power_name TEXT
);
```

### 2. MAC-SQL Schema (Planned)

A more descriptive format that includes table and column details, primary keys, and foreign key relationships in a commented, structured layout.

**Example (`superhero` database):**
```
[DB_ID] superhero
[Schema]
# Table: hero_power
(hero_id, hero id.),
(power_id, power id.)

# Table: superpower
(id, id.),
(power_name, power name, Value examples:['Agility'])

[Foreign keys]
hero_power.power_id = superpower.id
```

### 3. M-Schema (Planned)

A minimal, clean representation focusing on the essential structure, tables, and columns.

**Example (`superhero` database):**
```
[DB_ID] superhero
[Schema]
# Table: hero_power
(hero_id:INTEGER, Primary Key, the id of the hero, Maps to superhero(id), Examples:[1, 2, 3]),
(power_id:INTEGER, the id of the power, Maps to superpower(id), Examples:[1, 18, 26])

# Table: superpower
(id:INTEGER, Primary Key, the unique identifier of the superpower, Examples:[1, 2]),
(power_name:TEXT, the superpower name, Examples:['Agility', 'Accelerated Healing'])

[Foreign keys]
hero_power.hero_id = superhero.id
hero_power.power_id = superpower.id
```

## Roadmap

- [x] ✅ **Phase 1: DDL Schema Implementation**
  - Core database parsing logic using SQLAlchemy.
  - Generator for standard DDL `CREATE TABLE` statements.
- [ ] **Phase 2: MAC-SQL Schema**
  - Develop the generator for the detailed MAC-SQL format.
- [ ] **Phase 3: M-Schema**
  - Develop the generator for the compact M-Schema format.

## Contributing

Contributions are welcome! If you would like to help, please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

To add a new schema generator, you can create a new method within the schema generation class and expose it via the command-line interface in `main.py`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
