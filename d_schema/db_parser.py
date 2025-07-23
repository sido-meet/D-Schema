
from sqlalchemy import create_engine, inspect, MetaData

class DatabaseParser:
    """
    Connects to a database and extracts its metadata.
    """
    def __init__(self, db_url: str):
        """
        Initializes the parser with a database URL.

        Args:
            db_url: The SQLAlchemy database URL.
        """
        self.engine = create_engine(db_url)
        self.inspector = inspect(self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def get_metadata(self) -> MetaData:
        """
        Reflects the database and returns its metadata.

        Returns:
            A SQLAlchemy MetaData object containing the database structure.
        """
            
        return self.metadata
