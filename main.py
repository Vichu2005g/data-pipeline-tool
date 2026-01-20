import yaml
import os
import sys
from src.logger import setup_logger
from src.sql_utils import DatabaseManager
from src.ingestion import DataIngestor
from src.cleaning import DataCleaner
from src.analysis import TrendAnalyzer
from src.reporting import ReportGenerator

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
        cleaner = DataCleaner(logger)
        analyzer = TrendAnalyzer(logger, config)
        reporter = ReportGenerator(logger, config)
        logger.info("Infrastructure initialized (DB, Ingestion, Cleaning, Analysis, Reporting).")
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
            
            # --- STEP B: CLEANING ---
            df_clean = cleaner.clean_data(df_raw)
            logger.info(f"Data cleaned. Rows: {len(df_clean)}")

            # --- STEP C: STORAGE ---
            # Store cleaned data
            db.insert_data(df_clean, "cleaned_data_staging")
            
            # --- STEP D: ANALYSIS ---
            stats = analyzer.compute_stats(df_clean)
            anomalies = analyzer.detect_anomalies(df_clean)
            logger.info(f"Analysis complete. Found {len(anomalies)} anomalies.")
            
            # --- STEP E: REPORTING ---
            report_path = reporter.generate_report(df_clean, stats, anomalies, file_name)
            logger.info(f"Report generated: {report_path}")
            
            logger.info(f"Finished processing {file_name}.")
            
        except Exception as e:
            logger.error(f"Pipeline failed for {file_name}: {e}")

    logger.info("Pipeline Execution Finished.")

if __name__ == "__main__":
    main()