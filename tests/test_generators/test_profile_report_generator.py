import unittest
from tests.mock_schema import create_mock_schema
from d_schema.generators.profile_report.generator import ProfileReportGenerator

class TestProfileReportGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a mock DatabaseSchema object for testing."""
        self.mock_schema = create_mock_schema()
        self.generator = ProfileReportGenerator(self.mock_schema)

    def test_generate_profile_report(self):
        """Test the Profile-Report generation."""
        profile_report_output = self.generator.generate_schema()
        
        expected_output = """
# Data Profiling Report

### Table: `hero`
*Record Count: N/A*

| Column Name | Data Type | Profile Details |
|-------------|-----------|-----------------|
| id | INTEGER | *No profile data* |
| name | VARCHAR(100) | *No profile data* |

---

### Table: `superpower`
*Record Count: N/A*

| Column Name | Data Type | Profile Details |
|-------------|-----------|-----------------|
| id | INTEGER | *No profile data* |
| power_name | TEXT | *No profile data* |

---

### Table: `hero_power`
*Record Count: N/A*

| Column Name | Data Type | Profile Details |
|-------------|-----------|-----------------|
| hero_id | INTEGER | *No profile data* |
| power_id | INTEGER | *No profile data* |

---
"""
        self.maxDiff = None
        self.assertEqual(profile_report_output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
