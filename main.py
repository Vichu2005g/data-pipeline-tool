from src.logger import setup_logger
from src.sql_utils import DatabaseManager
from src.ingestion import DataIngestor
import pandas as pd
import os

def main():
    logger = setup_logger()
    logger.info("Starting Pipeline Test (Step 5: Ingestion)...")
    
    # 1. Test Database
    try:
        db = DatabaseManager()
        logger.info("Database connection verified.")
    except Exception as e:
        logger.error(f"DB Init failed: {e}")
        return

    # 2. Test Ingestion
    ingestor = DataIngestor(logger)
    
    # Create a dummy CSV for ingestion test
    dummy_csv = "data/raw/test_data.csv"
    os.makedirs(os.path.dirname(dummy_csv), exist_ok=True)
    with open(dummy_csv, "w") as f:
        f.write("id,value\n100,test_val_A\n101,test_val_B")
    
    try:
        logger.info(f"Testing ingestion from {dummy_csv}...")
        df = ingestor.ingest_file(dummy_csv)
        print("\n--- Ingested Data ---")
        print(df)
        print("---------------------\n")
        
        # 3. Store in DB
        db.insert_data(df, "ingested_test_table")
        logger.info("Ingested data stored in DB successfully.")
        
    except Exception as e:
        logger.error(f"Ingestion test failed: {e}")

if __name__ == "__main__":
    main()