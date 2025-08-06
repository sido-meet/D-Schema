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

# D-Schema

D-Schema is a versatile Python library and application designed to connect to a database, parse its structure, and generate various schema definitions. It uses Hydra for powerful and flexible configuration.

## Features

- **Dynamic Database Parsing**: Leverages `SQLAlchemy` to support a wide range of database backends.
- **Multiple Schema Formats**: Generate various types of schema definitions, including DDL, M-Schema, MAC-SQL, and a data profiling report.
- **Powerful Configuration**: Uses Hydra to allow easy configuration of database URLs, output paths, and generator-specific parameters from the command line.
- **Extensible by Design**: The internal structure makes it straightforward to add new schema generators.

## Installation

First, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the library and its dependencies using `pip`:

```bash
pip install -e .
```

## Usage

D-Schema is run as a Python module from the command line. It is configured using Hydra.

### Basic Usage

To run with the default configuration (generates a DDL schema for the test database), run:

```bash
python -m d_schema.app
```

This will generate a `schema.ddl` file in the `schema_output/` directory.

### Overriding Configuration

You can override any configuration parameter from the command line.

- **Change the database URL and output path:**
  ```bash
  python -m d_schema.app db_url="postgresql://user:pass@host/db" output_path="./my_schemas"
  ```

- **Run a different generator:**
  ```bash
  python -m d_schema.app generator=m_schema
  ```

### Running a Different Generator

To run a generator other than the default, override the `generator` parameter:

```bash
python -m d_schema.app generator=m_schema
```

To generate multiple schema formats, you will need to run the command multiple times with different `generator` values.

### Configuring Generator Parameters

You can change the parameters for a specific generator. For example, to generate a DDL schema without any comments:

```bash
python -m d_schema.app generator=ddl generator.allow_comments=false
```

Or to generate a DDL schema with only profiling info in the comments:

```bash
python -m d_schema.app generator=ddl generator.include_comment_text=false generator.include_examples=false
```

All configuration files can be found in the `conf/` directory.

## Project Structure

- `conf/`: Contains all Hydra configuration files.
- `src/d_schema/`: The main package source code.
  - `app.py`: The main Hydra application entry point.
  - `db_parser.py`: Database parsing logic.
  - `structures.py`: Core data structures.
  - `generators/`: Schema generator plugins.

## Programmatic Usage

While the command-line interface is convenient, `d-schema` is fundamentally a library. You can use its components directly in your own Python code for more complex workflows or integrations.

An example of programmatic usage can be found in `examples/programmatic_usage.py`.

Here is a brief overview:

```python
from d_schema import DatabaseParser, DDLSchemaGenerator

# 1. Initialize the parser and parse the database
parser = DatabaseParser(db_url="sqlite:///path/to/your.db")
db_structure = parser.parse(profile=True) # Enable profiling if needed

# 2. Initialize a generator with the parsed structure
# You can configure the generator directly
ddl_generator = DDLSchemaGenerator(
    schema=db_structure,
    allow_comments=False # Example: disable comments
)

# 3. Generate the content and save it
output_content = ddl_generator.generate_schema()
with open("my_schema.ddl", "w") as f:
    f.write(output_content)
```

This approach gives you full control over the parsing and generation process.


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
