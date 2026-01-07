import yaml
import os
import sys
from src.logger import setup_logger
from src.sql_utils import DatabaseManager
from src.ingestion import DataIngestor
# Future imports for Teammate's work:
# from src.cleaning import DataCleaner
# from src.analysis import TrendAnalyzer
# from src.reporting import ReportGenerator

def main():
    # 1. Setup Logging
    logger = setup_logger()
    logger.info("Starting Data Pipeline...")

    # 2. Load Config
    try:
        with open("config/config.yaml", "r") as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded.")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return

    # 3. Initialize Infrastructure Modules
    try:
        db = DatabaseManager(config["paths"]["db"])
        ingestor = DataIngestor(logger)
        logger.info("Infrastructure initialized (DB, Ingestion).")
    except Exception as e:
        logger.error(f"Infrastructure initialization failed: {e}")
        return

    # 4. Pipeline Execution
    raw_dir = config["paths"]["data_raw"]
    
    # Check for files
    if not os.path.exists(raw_dir):
        logger.error(f"Raw data directory not found: {raw_dir}")
        return

    files = [f for f in os.listdir(raw_dir) if f.endswith(('.csv', '.json'))]
    if not files:
        logger.warning(f"No data files found in {raw_dir}. Please add a file to process.")
        return

    for file_name in files:
        file_path = os.path.join(raw_dir, file_name)
        logger.info(f"Processing file: {file_path}")
        
        try:
            # --- STEP A: INGESTION ---
            df_raw = ingestor.ingest_file(file_path)
            
            # --- STEP B: CLEANING (TODO: Teammate) ---
            # df_clean = cleaner.clean_data(df_raw)
            # logger.info("Data cleaned.")

            # --- STEP C: STORAGE ---
            # Store raw data for audit (optional) or cleaned data later
            db.insert_data(df_raw, "raw_data_staging")
            
            # --- STEP D: ANALYSIS (TODO: Teammate) ---
            # insights = analyzer.analyze(df_clean)
            
            # --- STEP E: REPORTING (TODO: Teammate) ---
            # reporter.generate_report(insights)
            
            logger.info(f"Finished processing {file_name}.")
            
        except Exception as e:
            logger.error(f"Pipeline failed for {file_name}: {e}")

    logger.info("Pipeline Execution Finished.")

if __name__ == "__main__":
    main()