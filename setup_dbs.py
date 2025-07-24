# setup_dbs.py
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# --- Database Connection Details ---
DB_CONFIG = {
    "postgres": "postgresql://postgres:mysecretpassword@localhost:5432/postgres",
    "mysql_base": "mysql+mysqlconnector://root:mysecretpassword@localhost:3306/",
    "mysql_db": "mysql+mysqlconnector://root:mysecretpassword@localhost:3306/test_schema"
}

# --- Schema Definition (DDL) ---
# Using generic types that work across platforms
SCHEMA_DDL = """
CREATE TABLE IF NOT EXISTS hero (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS superpower (
    id INTEGER PRIMARY KEY,
    power_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS hero_power (
    hero_id INTEGER,
    power_id INTEGER,
    PRIMARY KEY (hero_id, power_id),
    FOREIGN KEY (hero_id) REFERENCES hero(id),
    FOREIGN KEY (power_id) REFERENCES superpower(id)
);
"""

def setup_mysql_database():
    """Creates the initial MySQL database and then sets up the schema."""
    try:
        # Connect to MySQL server without specifying a database
        base_engine = create_engine(DB_CONFIG["mysql_base"])
        with base_engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS test_schema"))
            print("Database 'test_schema' created or already exists.")
        
        # Connect to the specific database to create tables
        db_engine = create_engine(DB_CONFIG["mysql_db"])
        setup_database(db_engine)
    except Exception as e:
        print(f"An error occurred during MySQL setup: {e}")


def setup_database(engine):
    """Creates tables and inserts data in the given database."""
    dialect = engine.dialect.name
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # Using CREATE TABLE IF NOT EXISTS is safer for re-running the script
            for statement in SCHEMA_DDL.strip().split(';'):
                if statement.strip():
                    connection.execute(text(statement))
            
            # Insert sample data based on dialect
            if dialect == 'postgresql':
                connection.execute(text("INSERT INTO hero (id, name) VALUES (1, 'Superman') ON CONFLICT (id) DO NOTHING"))
                connection.execute(text("INSERT INTO superpower (id, power_name) VALUES (1, 'Flight') ON CONFLICT (id) DO NOTHING"))
                connection.execute(text("INSERT INTO superpower (id, power_name) VALUES (2, 'Super Strength') ON CONFLICT (id) DO NOTHING"))
            elif dialect == 'mysql':
                connection.execute(text("INSERT IGNORE INTO hero (id, name) VALUES (1, 'Superman')"))
                connection.execute(text("INSERT IGNORE INTO superpower (id, power_name) VALUES (1, 'Flight')"))
                connection.execute(text("INSERT IGNORE INTO superpower (id, power_name) VALUES (2, 'Super Strength')"))
            elif dialect == 'sqlite':
                connection.execute(text("INSERT OR IGNORE INTO hero (id, name) VALUES (1, 'Superman')"))
                connection.execute(text("INSERT OR IGNORE INTO superpower (id, power_name) VALUES (1, 'Flight')"))
                connection.execute(text("INSERT OR IGNORE INTO superpower (id, power_name) VALUES (2, 'Super Strength')"))

            # This will fail if the combination already exists, which is fine
            connection.execute(text("INSERT INTO hero_power (hero_id, power_id) VALUES (1, 1)"))
            connection.execute(text("INSERT INTO hero_power (hero_id, power_id) VALUES (1, 2)"))

            trans.commit()
            print(f"Successfully set up schema and data for {engine.url.database} on {engine.url.drivername}.")
        except Exception as e:
            print(f"An error occurred during schema setup for {engine.url.drivername}: {e}")
            trans.rollback()

def main():
    """Main function to set up all configured databases."""
    # Setup PostgreSQL
    print("--- Setting up POSTGRES ---")
    try:
        pg_engine = create_engine(DB_CONFIG["postgres"])
        setup_database(pg_engine)
    except Exception as e:
        print(f"An error occurred during PostgreSQL setup: {e}")

    # Setup MySQL
    print("\n--- Setting up MYSQL ---")
    setup_mysql_database()


if __name__ == "__main__":
    main()
