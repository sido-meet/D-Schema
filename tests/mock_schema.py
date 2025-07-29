from d_schema.structures import DatabaseSchema, TableInfo, ColumnInfo

def create_mock_schema():
    """Creates a mock DatabaseSchema object for testing."""
    return DatabaseSchema(
        db_name="test_db",
        tables=[
            TableInfo(
                name="hero",
                columns=[
                    ColumnInfo(name="id", type="INTEGER", nullable=False, primary_key=True, comment="the id of the hero", samples=['1']),
                    ColumnInfo(name="name", type="VARCHAR(100)", nullable=False, primary_key=False, comment="the name of the hero", samples=['Superman']),
                ]
            ),
            TableInfo(
                name="superpower",
                columns=[
                    ColumnInfo(name="id", type="INTEGER", nullable=False, primary_key=True, comment="the unique identifier of the superpower", samples=['1', '2']),
                    ColumnInfo(name="power_name", type="TEXT", nullable=True, primary_key=False, comment="the superpower name", samples=['Agility', 'Accelerated Healing']),
                ]
            ),
            TableInfo(
                name="hero_power",
                columns=[
                    ColumnInfo(name="hero_id", type="INTEGER", nullable=True, primary_key=False, foreign_key="REFERENCES hero(id)", comment="the id of the hero", samples=['1', '2', '3']),
                    ColumnInfo(name="power_id", type="INTEGER", nullable=True, primary_key=False, foreign_key="REFERENCES superpower(id)", comment="the id of the power", samples=['1', '18', '26']),
                ]
            )
        ]
    )
