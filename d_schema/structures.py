# d_schema/structures.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ColumnInfo:
    """
    Holds all relevant information about a database column.
    """
    name: str
    type: str
    nullable: bool
    primary_key: bool
    foreign_key: Optional[str] = None
    comment: Optional[str] = None
    samples: List[str] = field(default_factory=list)

@dataclass
class TableInfo:
    """
    Holds all relevant information about a database table.
    """
    name: str
    columns: List[ColumnInfo]

@dataclass
class DatabaseSchema:
    """
    Represents the entire database schema, independent of SQLAlchemy.
    """
    db_name: str
    tables: List[TableInfo]
