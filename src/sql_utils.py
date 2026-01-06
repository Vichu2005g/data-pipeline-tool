import sqlite3
import pandas as pd
import os
from sqlalchemy import create_engine

class DatabaseManager:
    def __init__(self, db_path="db/insights.db"):
        self.db_path = db_path
        self.conn_str = f"sqlite:///{self.db_path}"
        self._ensure_db_dir()

    def _ensure_db_dir(self):
        """Ensures the database directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_engine(self):
        """Returns a SQLAlchemy engine."""
        return create_engine(self.conn_str)

    def insert_data(self, df: pd.DataFrame, table_name: str, if_exists="replace"):
        """
        Inserts a DataFrame into the SQLite database.
        """
        engine = self.get_engine()
        try:
            df.to_sql(table_name, engine, index=False, if_exists=if_exists)
            print(f"Data inserted into table '{table_name}' successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def query_data(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query and returns a DataFrame.
        """
        engine = self.get_engine()
        try:
            return pd.read_sql(query, engine)
        except Exception as e:
            print(f"Error querying data: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    # Test the DB Manager
    db = DatabaseManager()
    df_test = pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})
    db.insert_data(df_test, "test_table")
    print(db.query_data("SELECT * FROM test_table"))
