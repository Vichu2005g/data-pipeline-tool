from src.logger import setup_logger
from src.sql_utils import DatabaseManager
import pandas as pd

def main():
    logger = setup_logger()
    logger.info("Starting Pipeline Test...")
    
    # Test Database Connection
    try:
        db = DatabaseManager()
        logger.info("Database connection established.")
        
        # Create dummy data
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "value": ["alpha", "beta", "gamma"]
        })
        
        # Insert into DB
        db.insert_data(df, "test_table")
        logger.info("Dummy data inserted.")
        
        # Query back
        result = db.query_data("SELECT * FROM test_table")
        logger.info(f"Query Result:\n{result}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    main()