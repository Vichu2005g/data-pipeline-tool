import pandas as pd
import os
import json

class DataIngestor:
    def __init__(self, logger):
        self.logger = logger

    def ingest_file(self, file_path: str) -> pd.DataFrame:
        """
        Reads a file (CSV or JSON) and returns a DataFrame.
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(file_path)
                self.logger.info(f"Successfully loaded CSV: {file_path} with {len(df)} rows.")
                return df
            elif ext == ".json":
                df = pd.read_json(file_path)
                self.logger.info(f"Successfully loaded JSON: {file_path} with {len(df)} rows.")
                return df
            else:
                self.logger.error(f"Unsupported file format: {ext}")
                raise ValueError(f"Unsupported file format: {ext}")
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            raise
