import pandas as pd
import numpy as np
from scipy import stats

class TrendAnalyzer:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.anomaly_threshold = config.get("processing", {}).get("anomaly_threshold", 2.0)
        self.rolling_window = config.get("processing", {}).get("rolling_window", 7)

    def compute_stats(self, df: pd.DataFrame) -> dict:
        """
        Computes basic statistics for numeric columns.
        Returns a dictionary with summary stats.
        """
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                self.logger.warning("No numeric columns found for analysis.")
                return {}

            stats_summary = {}
            for col in numeric_cols:
                stats_summary[col] = {
                    "mean": df[col].mean(),
                    "median": df[col].median(),
                    "std": df[col].std(),
                    "min": df[col].min(),
                    "max": df[col].max()
                }
            
            self.logger.info(f"Computed statistics for {len(numeric_cols)} numeric columns.")
            return stats_summary
            
        except Exception as e:
            self.logger.error(f"Error computing statistics: {e}")
            raise

    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detects anomalies using Z-score method.
        Returns a DataFrame of rows flagged as anomalies.
        """
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                self.logger.warning("No numeric columns for anomaly detection.")
                return pd.DataFrame()

            anomalies = pd.DataFrame()
            for col in numeric_cols:
                z_scores = np.abs(stats.zscore(df[col].fillna(0)))
                anomaly_mask = z_scores > self.anomaly_threshold
                col_anomalies = df[anomaly_mask].copy()
                col_anomalies['anomaly_column'] = col
                col_anomalies['z_score'] = z_scores[anomaly_mask]
                anomalies = pd.concat([anomalies, col_anomalies], ignore_index=True)

            self.logger.info(f"Detected {len(anomalies)} anomalies (Z-score > {self.anomaly_threshold}).")
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {e}")
            raise

    def compute_rolling_average(self, df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
        """
        Computes rolling average for time-series data.
        Requires a date column and a numeric value column.
        """
        try:
            if date_col not in df.columns or value_col not in df.columns:
                self.logger.warning(f"Columns {date_col} or {value_col} not found. Skipping rolling average.")
                return df

            df_sorted = df.sort_values(by=date_col).copy()
            df_sorted[f'{value_col}_rolling_avg'] = df_sorted[value_col].rolling(
                window=self.rolling_window, min_periods=1
            ).mean()
            
            self.logger.info(f"Computed {self.rolling_window}-period rolling average for {value_col}.")
            return df_sorted
            
        except Exception as e:
            self.logger.error(f"Error computing rolling average: {e}")
            raise
