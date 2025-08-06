"""
D-Schema: Database Schema Generation and Analysis Toolkit
"""

__version__ = "0.2.0" # Bump version for new features

# Public API: Expose the core data structures and the parser
from .structures import (
    DatabaseSchema,
    TableInfo,
    ColumnInfo,
    TableProfile,
    ColumnProfile,
)
from .db_parser import DatabaseParser

# Expose the generator classes for programmatic use
from .generators.ddl_schema.generator import DDLSchemaGenerator
from .generators.m_schema.generator import MSchemaGenerator
from .generators.mac_sql_schema.generator import MacSQLSchemaGenerator
from .generators.profile_report.generator import ProfileReportGenerator


__all__ = [
    "DatabaseSchema",
    "TableInfo",
    "ColumnInfo",
    "TableProfile",
    "ColumnProfile",
    "DatabaseParser",
    "DDLSchemaGenerator",
    "MSchemaGenerator",
    "MacSQLSchemaGenerator",
    "ProfileReportGenerator",
]
