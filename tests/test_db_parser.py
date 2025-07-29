import unittest
from d_schema.db_parser import DatabaseParser

class TestDatabaseParser(unittest.TestCase):
    def test_parse_sqlite_in_memory(self):
        """Test parsing an in-memory SQLite database."""
        try:
            parser = DatabaseParser(db_url="sqlite:///:memory:")
            parser.parse()
        except Exception as e:
            self.fail(f"DatabaseParser failed to parse in-memory SQLite DB: {e}")

if __name__ == '__main__':
    unittest.main()
