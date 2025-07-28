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
- `d_schema/generators/`: A package directory containing the schema generator plugins. Each subdirectory is a self-contained plugin for a specific schema format (e.g., `ddl_schema`, `m_schema`).
  - `base_generator.py`: Defines the `BaseGenerator` abstract class that all plugins must inherit from.
- `d_schema/main.py`: The command-line interface that dynamically discovers and runs the generator plugins.

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
d-schema --db-url "sqlite:///test_data/test.db" --schema-type mac-sql-schema --profile
```

- `--db-url`: The SQLAlchemy database URL for the target database.
- `--schema-type`: The type of schema to generate. Use `d-schema --help` to see a full list of available generator plugins.
- `--profile`: (Optional) Enables detailed data profiling. This can be slow on large databases but enriches the schema with valuable statistics.

## Testing

For detailed information on how to run the tests for this project, please see the [Testing Documentation](./tests/README.md).

## Schema Formats

This project supports multiple schema output formats. For detailed explanations and examples of each format, please see the [Schema Formats Documentation](./d_schema/generators/README.md).

## Roadmap

- [x] **Phase 1: DDL Schema Implementation**
  - Core database parsing logic using SQLAlchemy.
  - Generator for standard DDL `CREATE TABLE` statements.
- [x] **Phase 2: MAC-SQL Schema**
  - Develop the generator for the detailed MAC-SQL format.
- [x] **Phase 3: M-Schema**
  - Develop the generator for the compact M-Schema format.
- [x] **Phase 4: Database Profiling**
  - **Statistical Analysis**: Enhance the `DatabaseParser` to compute and store key statistics.
    - Table-level: record count.
    - Column-level: NULL vs. non-NULL count, distinct value count, min/max values, character length (min/max/avg), and alphabet analysis (e.g., upper/lower/punctuation).
  - **Data Shape & Sketches**:
    - Capture the "shape" of fields to provide deeper insights into data patterns.
    - Generate and store a sample of the top-k most frequent values for each column.
    - Implement MinHash sketching for efficient similarity comparisons.
  - **Schema Integration**: Update the `DatabaseSchema` structure to store this metadata and integrate it into the schema generators as non-invasive annotations or as a dedicated profiling report.
- [ ] **Phase 5: AI-Powered Schema Enrichment**
  - Implement an `AIEnricher` module to intelligently enhance schema details, using the rich context from the profiling phase.
  - **Column Comment Generation**: Automatically generate comments for columns where they are missing, using column name, type, and data samples as context for an LLM.
  - **Name Clarification**: For tables or columns with ambiguous or abbreviated names (e.g., `cust_ord_dtl`), use an LLM to infer and generate a natural language explanation of its likely business purpose.
- [ ] **Phase 6: Advanced Features & Integrations**
  - **Relationship Inference**: Detect and suggest potential relationships between tables that lack formal foreign key constraints.
  - **Data Anonymization**: Add an option to anonymize sensitive data found in column samples.
  - **New Export Formats**: Extend generation to support formats like JSON Schema, GraphQL Schema, or Graphviz visualization.

## Contributing

Contributions are welcome! If you would like to help, please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

To add a new schema generator, simply create a new subdirectory in `d_schema/generators/`. The directory name will be used as the `--schema-type` argument (e.g., `new_format` for `d_schema/generators/new_format/`). Inside this new directory, create a `generator.py` file containing a class that inherits from `BaseGenerator` and implements the required methods. The `main.py` script will automatically discover and integrate your new plugin.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.