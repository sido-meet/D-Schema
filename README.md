# D-Schema

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

D-Schema is a versatile Python tool designed to connect to a database, parse its structure, and generate various schema definitions. It can be used both as a flexible command-line application powered by Hydra, and as a library in your own Python projects.

## Features

- **Dynamic Database Parsing**: Leverages `SQLAlchemy` to support a wide range of database backends (PostgreSQL, MySQL, SQLite, etc.).
- **Multiple Schema Formats**: Generate various schema definitions, including:
  - Standard SQL DDL (`CREATE TABLE` statements)
  - M-Schema and MAC-SQL for analysis
  - A detailed Markdown data profiling report
- **Powerful Configuration**: Uses Hydra to allow easy configuration of all parameters from the command line.
- **Extensible by Design**: The internal structure makes it straightforward to add new schema generators.
- **Dual Usage**: Can be run as a command-line tool or imported as a Python library.

## Installation

First, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the library and its dependencies from the project root:

```bash
pip install -e .
```

## Usage

D-Schema offers two primary ways to use it.

### 1. Command-Line (via Hydra)

This is the easiest way to get started. The application is run as a Python module and configured with command-line arguments.

**Basic Usage**

To run with the default configuration (generates a DDL schema for the test database):
```bash
python -m d_schema.app
```
This will generate a `schema.ddl` file in the `schema_output/` directory.

**Overriding Configuration**

You can override any parameter defined in the `src/d_schema/config/` directory.

- **Use a different generator and database:**
  ```bash
  python -m d_schema.app generator=profile_report db_url="postgresql://user:pass@host/db"
  ```

- **Change the number of sample values fetched:**
  ```bash
  python -m d_schema.app num_samples=10
  ```

- **Configure DDL generator parameters (e.g., disable comments):**
  ```bash
  python -m d_schema.app generator=ddl generator.allow_comments=false
  ```

### 2. As a Library (Programmatic Usage)

For more complex workflows or integration into other applications, you can import and use the core components of `d-schema` directly.

An example is provided in `examples/programmatic_usage.py`.

**Quick Overview:**

```python
from d_schema import DatabaseParser, DDLSchemaGenerator

# 1. Initialize the parser and parse the database
# Control the number of samples fetched during parsing.
parser = DatabaseParser(db_url="sqlite:///path/to/your.db")
db_structure = parser.parse(profile=True, num_samples=5)

# 2. Initialize a generator with the parsed structure
# You can configure the generator's parameters directly.
ddl_generator = DDLSchemaGenerator(
    schema=db_structure,
    allow_comments=False # Example: disable comments
)

# 3. Generate the content and save it
output_content = ddl_generator.generate_schema()
with open("my_schema.ddl", "w") as f:
    f.write(output_content)
```

## Contributing

Contributions are welcome! To add a new schema generator:

1.  Create a new generator class inheriting from `BaseGenerator` in the `src/d_schema/generators/` directory.
2.  Add it to the `GENERATOR_CLASSES` dictionary in `src/d_schema/app.py`.
3.  Create a corresponding configuration file in `src/d_schema/config/generator/` (e.g., `new_format.yaml`).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.