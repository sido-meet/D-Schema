# d_schema/structures.py
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class ColumnProfile:
    """
    Contains statistical and analytical data about a column.
    """
    null_count: Optional[int] = None
    non_null_count: Optional[int] = None
    distinct_count: Optional[int] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    avg_char_length: Optional[float] = None
    top_k_values: List[Tuple[str, int]] = field(default_factory=list)
    minhash_sketch: Optional[bytes] = None


@dataclass
class TableProfile:
    """
    Contains statistical data about a table.
    """
    record_count: Optional[int] = None


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
    profile: Optional[ColumnProfile] = None


@dataclass
class TableInfo:
    """
    Holds all relevant information about a database table.
    """
    name: str
    columns: List[ColumnInfo]
    profile: Optional[TableProfile] = None


@dataclass
class DatabaseSchema:
    """
    Represents the entire database schema, independent of SQLAlchemy.
    """
    db_name: str
    tables: List[TableInfo]
