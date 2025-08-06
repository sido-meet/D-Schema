# d_schema/db_parser.py

import os
from sqlalchemy import create_engine, inspect, select, distinct, func, MetaData, String, Date
from sqlalchemy.exc import SQLAlchemyError
from datasketch import MinHash, LeanMinHash
from .structures import (
    DatabaseSchema,
    TableInfo,
    ColumnInfo,
    TableProfile,
    ColumnProfile,
)

class DatabaseParser:
    """
    Connects to a database and extracts its structure into a self-contained format.
    """

    def __init__(self, db_url: str):
        """
        Initializes the parser with a database URL.

        Args:
            db_url: The SQLAlchemy database URL.
        """
        self.engine = create_engine(db_url)

    def parse(self, profile: bool = False, num_samples: int = 5) -> DatabaseSchema:
        """
        Parses the database and returns a DatabaseSchema object.

        Args:
            profile: If True, performs detailed profiling of the data.

        Returns:
            A DatabaseSchema object containing the database structure.
        """
        db_name = self.engine.url.database
        # For SQLite, the database name is the file path. Let's just get the filename without the extension.
        if self.engine.dialect.name == 'sqlite':
            basename = os.path.basename(db_name)
            db_name, _ = os.path.splitext(basename)

        tables_info = []
        inspector = inspect(self.engine)
        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        table_names = inspector.get_table_names()

        with self.engine.connect() as connection:
            for table_name in table_names:
                columns_info = []
                pk_constraint = inspector.get_pk_constraint(table_name)
                primary_keys = pk_constraint.get("constrained_columns", [])
                columns = inspector.get_columns(table_name)
                foreign_keys = inspector.get_foreign_keys(table_name)

                meta_table = metadata.tables.get(table_name)
                if meta_table is None:
                    print(f"Could not find table '{table_name}' in reflected metadata. Skipping.")
                    continue

                for column in columns:
                    is_primary_key = column["name"] in primary_keys
                    fk_info = next(
                        (
                            fk
                            for fk in foreign_keys
                            if column["name"] in fk["constrained_columns"]
                        ),
                        None,
                    )
                    foreign_key_str = (
                        f"REFERENCES {fk_info['referred_table']}({fk_info['referred_columns'][0]})"
                        if fk_info
                        else None
                    )

                    # Fetch sample values
                    try:
                        meta_column = meta_table.c[column["name"]]
                        if isinstance(column["type"], Date):
                            query = (
                                select(meta_column.cast(String))
                                .distinct()
                                .where(meta_column.isnot(None))
                                .limit(num_samples)
                            )
                        else:
                            query = (
                                select(meta_column)
                                .distinct()
                                .where(meta_column.isnot(None))
                                .limit(num_samples)
                            )
                        result = connection.execute(query)
                        samples = [str(row[0]) for row in result]
                    except SQLAlchemyError as e:
                        print(
                            f"Could not fetch samples for {table_name}.{column['name']}: {e}"
                        )
                        samples = []

                    columns_info.append(
                        ColumnInfo(
                            name=column["name"],
                            type=str(column["type"]),
                            nullable=column["nullable"],
                            primary_key=is_primary_key,
                            foreign_key=foreign_key_str,
                            comment=column.get("comment"),
                            samples=samples,
                        )
                    )

                table_info = TableInfo(name=table_name, columns=columns_info)

                if profile:
                    self._profile_table_and_columns(
                        connection, table_info, meta_table
                    )

                tables_info.append(table_info)

        return DatabaseSchema(db_name=db_name, tables=tables_info)

    def _profile_table_and_columns(self, connection, table_info: TableInfo, meta_table):
        """
        Performs data profiling for a given table and its columns.
        """
        table_name = table_info.name
        print(f"Profiling table: {table_name}...")

        # Table-level profiling
        try:
            record_count = connection.execute(
                select(func.count()).select_from(meta_table)
            ).scalar_one()
            table_info.profile = TableProfile(record_count=record_count)
        except SQLAlchemyError as e:
            print(f"  - Could not get record count for {table_name}: {e}")
            return # Stop if we can't even get the count

        if record_count == 0:
            print("  - Table is empty, skipping column profiling.")
            return

        # Column-level profiling
        for column_info in table_info.columns:
            col_name = column_info.name
            meta_column = meta_table.c[col_name]
            col_profile = ColumnProfile()

            try:
                # Null/Non-null count
                null_count = connection.execute(
                    select(func.count())
                    .select_from(meta_table)
                    .where(meta_column.is_(None))
                ).scalar_one()
                col_profile.null_count = null_count
                col_profile.non_null_count = record_count - null_count

                # Distinct count
                distinct_count = connection.execute(
                    select(func.count(distinct(meta_column)))
                ).scalar_one()
                col_profile.distinct_count = distinct_count

                # Min/Max values (only for non-null values)
                if col_profile.non_null_count > 0:
                    min_max_query = select(func.min(meta_column), func.max(meta_column))
                    min_val, max_val = connection.execute(min_max_query).first()
                    col_profile.min_value = str(min_val) if min_val is not None else None
                    col_profile.max_value = str(max_val) if max_val is not None else None

                # String length analysis (for text-like types)
                if "CHAR" in str(column_info.type) or "TEXT" in str(column_info.type):
                    avg_len_query = select(func.avg(func.length(meta_column)))
                    avg_len = connection.execute(avg_len_query).scalar_one()
                    col_profile.avg_char_length = float(avg_len) if avg_len else 0.0

                # Top-K frequent values
                top_k_query = (
                    select(meta_column, func.count().label("freq"))
                    .where(meta_column.isnot(None))
                    .group_by(meta_column)
                    .order_by(func.count().desc())
                    .limit(10)
                )
                top_k_result = connection.execute(top_k_query)
                col_profile.top_k_values = [
                    (str(row[0]), row[1]) for row in top_k_result
                ]

                # MinHash sketch
                m = MinHash(num_perm=128)
                # Use streaming results to avoid loading all data into memory
                stream_query = select(meta_column).where(meta_column.isnot(None))
                for row in connection.execute(stream_query):
                    m.update(str(row[0]).encode("utf8"))
                
                # Convert to LeanMinHash for efficient serialization
                lean_m = LeanMinHash(m)
                buffer = bytearray(lean_m.bytesize())
                lean_m.serialize(buffer)
                col_profile.minhash_sketch = buffer

            except SQLAlchemyError as e:
                print(f"  - Could not fully profile column {table_name}.{col_name}: {e}")
            except Exception as e:
                print(f"  - An unexpected error occurred during profiling of {table_name}.{col_name}: {e}")


            column_info.profile = col_profile
