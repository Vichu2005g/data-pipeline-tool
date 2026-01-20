import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, logger):
        self.logger = logger

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            initial_count = len(df)
            df = df.drop_duplicates()
            if initial_count != len(df):
                self.logger.info(f"Removed {initial_count - len(df)} duplicates.")

            for col in df.columns:
                if df[col].dtype in [np.float64, np.int64]:
                    df[col] = df[col].fillna(0)
                else:
                    df[col] = df[col].fillna("Unknown")

            df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
            self.logger.info("Data cleaning completed.")
            return df
        except Exception as e:
            self.logger.error(f"Cleaning error: {e}")
            raise
