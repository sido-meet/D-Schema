import unittest
from tests.mock_schema import create_mock_schema
from d_schema.generators.ddl_schema.generator import DDLSchemaGenerator

class TestDDLSchemaGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a mock DatabaseSchema object for testing."""
        self.mock_schema = create_mock_schema()
        self.generator = DDLSchemaGenerator(self.mock_schema)

    def test_generate_ddl_schema(self):
        """Test the DDL-Schema generation."""
        ddl_schema_output = self.generator.generate_schema()
        
        expected_output = """
# Table: hero
CREATE TABLE hero (
    id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)

);

# Table: superpower
CREATE TABLE superpower (
    id INTEGER NOT NULL,
    power_name TEXT,
    PRIMARY KEY (id)

);

# Table: hero_power
CREATE TABLE hero_power (
    hero_id INTEGER,
    power_id INTEGER,
    FOREIGN KEY (hero_id) REFERENCES hero(id),
    FOREIGN KEY (power_id) REFERENCES superpower(id)

);
"""
        self.assertEqual(ddl_schema_output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
