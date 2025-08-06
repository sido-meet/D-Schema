# D-Schema

D-Schema is a versatile Python library designed to connect to a given database, parse its structure, and generate various database schema definitions. The project is architected to be highly modular, with a clear separation between database parsing and schema generation. This flexible design allows for easy extension to support new schema types in the future.

## Features

- **Dynamic Database Parsing**: Leverages `SQLAlchemy` to support a wide range of database backends (including SQLite, PostgreSQL, MySQL, etc.).
- **Multiple Schema Formats**: Generate various types of schema definitions from a single database source.
  - **DDL Schema**: Standard `CREATE TABLE` SQL statements.
  - **M-Schema**: A compact, human-readable format for analysis.
  - **MAC-SQL Schema**: A detailed, commented format.
  - **Profiling Report**: A Markdown report with detailed statistics about the data.
- **Extensible by Design**: The internal structure makes it straightforward to add new schema generators.

## Installation

First, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the library using `pip`. You can install it directly from this repository for development purposes:

```bash
pip install -e .
```

## Usage

`d-schema` is designed to be used as a library. The main entry point is the `d_schema.generate()` function.

A complete, runnable example can be found in the `examples/` directory. Here is a brief overview of how to use it:

```python
import d_schema
import os

# 1. Define your database connection URL and output path
DB_URL = "sqlite:///test_data/test.db" 
OUTPUT_DIR = "./schema_output"

# 2. Specify which generators you want to run
GENERATORS_TO_RUN = ["ddl", "m_schema", "profile_report"]

# 3. Run the generation process
d_schema.generate(
    db_url=DB_URL,
    output_path=OUTPUT_DIR,
    generators=GENERATORS_TO_RUN
)
```

To run the example script from the project root, use the following command:

```bash
# Make sure you have installed the project with `pip install -e .`
python examples/example.py
```

This will create the `schema_output` directory and place the generated files inside.

## Project Structure

The project is organized using a `src` layout:

- `src/d_schema/`: The main package source code.
  - `__init__.py`: Defines the public API, including the main `generate()` function.
  - `structures.py`: Defines the `dataclass` structures that represent the database schema.
  - `db_parser.py`: Contains the logic for connecting to the database and parsing its structure.
  - `generators/`: A package containing the schema generator plugins.
    - `base_generator.py`: Defines the `BaseGenerator` abstract class.

## Testing

For detailed information on how to run the tests for this project, please see the [Testing Documentation](./tests/README.md).

## Contributing

Contributions are welcome! To add a new schema generator:

1.  Create a new subdirectory in `src/d_schema/generators/`.
2.  Inside your new directory, create a `generator.py` file.
3.  In `generator.py`, define a class that inherits from `d_schema.generators.base_generator.BaseGenerator`.
4.  Implement the required methods, especially `generate_schema(self) -> str`.
5.  Register your new generator in `src/d_schema/__init__.py` by adding it to the `AVAILABLE_GENERATORS` dictionary.

## License

This project is licensed under the MIT License.
