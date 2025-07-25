import unittest
from d_schema.structures import DatabaseSchema, TableInfo, ColumnInfo
from d_schema.schema_generator import SchemaGenerator

class TestSchemaGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a mock DatabaseSchema object for testing."""
        self.mock_schema = DatabaseSchema(
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
        self.generator = SchemaGenerator(self.mock_schema)

    def test_generate_m_schema(self):
        """Test the M-Schema generation."""
        m_schema_output = self.generator.generate_m_schema()
        
        expected_output = """
[DB_ID] test_db

[Schema]
# Table: hero
(id:INTEGER, Primary Key, the id of the hero, Examples:[1])
(name:VARCHAR(100), the name of the hero, Examples:[Superman])

# Table: superpower
(id:INTEGER, Primary Key, the unique identifier of the superpower, Examples:[1, 2])
(power_name:TEXT, the superpower name, Examples:[Agility, Accelerated Healing])

# Table: hero_power
(hero_id:INTEGER, the id of the hero, Maps to hero(id), Examples:[1, 2, 3])
(power_id:INTEGER, the id of the power, Maps to superpower(id), Examples:[1, 18, 26])

[Foreign keys]
hero_power.hero_id = hero.id
hero_power.power_id = superpower.id
"""
        self.assertEqual(m_schema_output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()