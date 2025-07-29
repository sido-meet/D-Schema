import unittest
from tests.mock_schema import create_mock_schema
from d_schema.generators.mac_sql_schema.generator import MacSQLSchemaGenerator

class TestMacSQLSchemaGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a mock DatabaseSchema object for testing."""
        self.mock_schema = create_mock_schema()
        self.generator = MacSQLSchemaGenerator(self.mock_schema)

    def test_generate_mac_sql_schema(self):
        """Test the MAC-SQL-Schema generation."""
        mac_sql_output = self.generator.generate_schema()
        
        expected_output = """
# Table: hero
[
(id, the id of the hero. Value examples: ['1'].)
(name, the name of the hero. Value examples: ['Superman'].)
]

# Table: superpower
[
(id, the unique identifier of the superpower. Value examples: ['1', '2'].)
(power_name, the superpower name. Value examples: ['Agility', 'Accelerated Healing'].)
]

# Table: hero_power
[
(hero_id, the id of the hero. Value examples: ['1', '2', '3'].)
(power_id, the id of the power. Value examples: ['1', '18', '26'].)
]
"""
        self.assertEqual(mac_sql_output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
