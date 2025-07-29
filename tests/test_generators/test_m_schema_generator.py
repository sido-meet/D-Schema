import unittest
from tests.mock_schema import create_mock_schema
from d_schema.generators.m_schema.generator import MSchemaGenerator

class TestMSchemaGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a mock DatabaseSchema object for testing."""
        self.mock_schema = create_mock_schema()
        self.generator = MSchemaGenerator(self.mock_schema)

    def test_generate_m_schema(self):
        """Test the M-Schema generation."""
        m_schema_output = self.generator.generate_schema()
        
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
