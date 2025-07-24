# d_schema/db_parser.py

from sqlalchemy import create_engine, inspect, select, distinct, MetaData
from .structures import DatabaseSchema, TableInfo, ColumnInfo

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
        self.inspector = inspect(self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def parse(self) -> DatabaseSchema:
        """
        Parses the database and returns a DatabaseSchema object.

        Returns:
            A DatabaseSchema object containing the database structure.
        """
        db_name = self.engine.url.database
        tables_info = []
        
        table_names = self.inspector.get_table_names()

        with self.engine.connect() as connection:
            for table_name in table_names:
                columns_info = []
                pk_constraint = self.inspector.get_pk_constraint(table_name)
                primary_keys = pk_constraint.get('constrained_columns', [])
                
                columns = self.inspector.get_columns(table_name)
                foreign_keys = self.inspector.get_foreign_keys(table_name)

                for column in columns:
                    # Determine if the column is a primary key
                    is_primary_key = column['name'] in primary_keys

                    # Find foreign key information
                    fk_info = next((fk for fk in foreign_keys if column['name'] in fk['constrained_columns']), None)
                    foreign_key_str = None
                    if fk_info:
                        foreign_key_str = f"REFERENCES {fk_info['referred_table']}({fk_info['referred_columns'][0]})"

                    # Fetch sample values
                    try:
                        # Use the actual column object from the metadata for querying
                        meta_table = self.metadata.tables[table_name]
                        meta_column = meta_table.c[column['name']]
                        query = select(distinct(meta_column)).where(meta_column.isnot(None)).limit(5)
                        result = connection.execute(query)
                        samples = [str(row[0]) for row in result]
                    except Exception as e:
                        print(f"Could not fetch samples for {table_name}.{column['name']}: {e}")
                        samples = []

                    columns_info.append(ColumnInfo(
                        name=column['name'],
                        type=str(column['type']),
                        nullable=column['nullable'],
                        primary_key=is_primary_key,
                        foreign_key=foreign_key_str,
                        comment=column.get('comment'),
                        samples=samples
                    ))
                
                tables_info.append(TableInfo(name=table_name, columns=columns_info))

        return DatabaseSchema(db_name=db_name, tables=tables_info)
