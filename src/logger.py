import logging
import os
import yaml

def setup_logger(config_path="config/config.yaml"):
    """
    Sets up a logger that writes to both console and a file defined in config.
    """
    # Load config to get log path
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            log_path = config.get("paths", {}).get("logs", "logs/pipeline.log")
    else:
        log_path = "logs/pipeline.log"

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("DataPipeline")
    logger.info("Logger initialized.")
    return logger

if __name__ == "__main__":
    # Test the logger
    logger = setup_logger()
    logger.info("Test INFO message")
    logger.warning("Test WARNING message")
