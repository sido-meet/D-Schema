import unittest
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, ForeignKey
from d_schema.schema_generator import SchemaGenerator

class TestSchemaGenerator(unittest.TestCase):
    """
    Tests for the SchemaGenerator class.
    """
    def setUp(self):
        """
        Set up a temporary in-memory SQLite database for testing.
        """
        self.engine = create_engine("sqlite:///:memory:")
        self.metadata = MetaData()

        # Define a simple schema for testing
        self.superpower = Table('superpower', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('power_name', Text)
        )

        self.hero = Table('hero', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50), nullable=False)
        )

        self.hero_power = Table('hero_power', self.metadata,
            Column('hero_id', Integer, ForeignKey('hero.id')),
            Column('power_id', Integer, ForeignKey('superpower.id'))
        )
        
        # Create the tables in the in-memory database
        self.metadata.create_all(self.engine)

    def test_generate_ddl_schema(self):
        """
        Test the generation of a DDL schema.
        """
        schema_generator = SchemaGenerator(metadata=self.metadata)
        ddl_schema = schema_generator.generate_ddl_schema(engine=self.engine)

        # Expected DDL for the 'superpower' table
        expected_superpower_ddl = (
            "CREATE TABLE superpower (\n"
            "\tid INTEGER NOT NULL,\n"
            "\tpower_name TEXT,\n"
            "\tPRIMARY KEY (id)\n"
            ");"
        )

        # Expected DDL for the 'hero_power' table
        expected_hero_power_ddl = (
            "CREATE TABLE hero_power (\n"
            "\thero_id INTEGER,\n"
            "\tpower_id INTEGER,\n"
            "\tFOREIGN KEY(hero_id) REFERENCES hero (id),\n"
            "\tFOREIGN KEY(power_id) REFERENCES superpower (id)\n"
            ");"
        )
        
        self.assertIn("# Table: superpower", ddl_schema)
        self.assertIn(expected_superpower_ddl, ddl_schema)
        self.assertIn("# Table: hero_power", ddl_schema)
        self.assertIn(expected_hero_power_ddl, ddl_schema)

    def test_generate_mac_sql_schema(self):
        """
        Test the generation of a MAC-SQL schema.
        """
        schema_generator = SchemaGenerator(metadata=self.metadata, db_name="test_db")
        mac_sql_schema = schema_generator.generate_mac_sql_schema()

        expected_output = (
            "[DB_ID] test_db\n"
            "[Schema]\n"
            "[\n"
            "# Table: superpower\n"
            "(id, id.)\n"
            "(power_name, power_name.)\n"
            "# Table: hero\n"
            "(id, id.)\n"
            "(name, name.)\n"
            "# Table: hero_power\n"
            "(hero_id, hero_id.)\n"
            "(power_id, power_id.)\n"
            "]"
        )
        
        self.assertEqual(mac_sql_schema.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
