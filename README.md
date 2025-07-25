# D-Schema

D-Schema is a versatile Python-based tool designed to connect to a given database, parse its structure, and generate various database schema definitions. The project is architected to be highly modular, with a clear separation between database parsing and schema generation. This flexible design allows for easy extension to support new schema types in the future.

## Features

- **Dynamic Database Parsing**: Leverages `SQLAlchemy` to support a wide range of database backends (including SQLite, PostgreSQL, MySQL, etc.).
- **Multiple Schema Formats**: Designed to generate various types of schema definitions from a single database source.
  - **Currently Implemented**:
    - `DDL Schema`: The standard `CREATE TABLE` SQL statements.
    - `MAC-SQL Schema`: A detailed, commented format suitable for analysis.
    - `M-Schema`: A compact, human-readable format.
  - **Planned**:
- **Extensible by Design**: The internal class structure makes it straightforward to add new schema generators.

## Project Structure

The project is organized into the following key modules:

- `d_schema/structures.py`: Defines the `dataclass` structures that represent the database schema in a vendor-neutral format.
- `d_schema/db_parser.py`: Contains the `DatabaseParser` class, which connects to the database, extracts the schema, and populates the `dataclass` structures.
- `d_schema/schema_generator.py`: Contains the `SchemaGenerator` class, which takes the populated `dataclass` structures and generates the final schema string.
- `d_schema/main.py`: The command-line interface that ties everything together.

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
d-schema --db-url "sqlite:///test_data/test.db" --schema-type mac-sql
```

- `--db-url`: The SQLAlchemy database URL for the target database.
- `--schema-type`: The type of schema to generate. Currently supports `ddl`, `mac-sql`, and `m-schema`.

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
This will run the DDL and MAC-SQL generation for SQLite, PostgreSQL, and MySQL, allowing you to verify the output for each.

## Schema Formats Explained

This section provides examples of the different schema formats that D-Schema aims to support, using a sample `superhero` database.

### 1. DDL Schema

Standard SQL Data Definition Language (DDL) statements. This format is ideal for recreating the database structure.

**Example (`superhero` database):**
```sql
# Table: hero
CREATE TABLE hero (
    id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
```

### 2. MAC-SQL Schema

A more descriptive format that includes table and column details, primary keys, and foreign key relationships in a commented, structured layout.

**Example (`superhero` database):**
```
# Table: hero
[
(id, the id of the hero. Value examples: ['1'].)
(name, the name of the hero. Value examples: ['Superman'].)
]
```

### 3. M-Schema

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

- [x] **Phase 1: DDL Schema Implementation**
  - Core database parsing logic using SQLAlchemy.
  - Generator for standard DDL `CREATE TABLE` statements.
- [x] **Phase 2: MAC-SQL Schema**
  - Develop the generator for the detailed MAC-SQL format.
- [x] **Phase 3: M-Schema**
  - Develop the generator for the compact M-Schema format.

## Contributing

Contributions are welcome! If you would like to help, please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

To add a new schema generator, you can create a new method within the `SchemaGenerator` class in `d_schema/schema_generator.py` and expose it via the command-line interface in `d_schema/main.py`. The generator should only rely on the `DatabaseSchema` object passed to its constructor.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.