# Automated Data Pipeline & Insights Reporting Tool

A production-grade Python system designed to ingest raw data, process it for analytical quality, and generate automated business intelligence reports.

## Overview

This tool simulates a real-world Enterprise Data Engineering pipeline. It eliminates manual data handling by automating the flow from raw ingestion to final reporting. It is built with modularity, scalability, and observability in mind, mimicking the architecture used by data teams at major organizations.

**Key Capabilities:**
*   **Automated Ingestion**: Seamlessly loads CSV and JSON data from raw landing zones.
*   **Data Quality Engine**: Automatically handles missing values, duplicates, and type enforcement.
*   **Analytical Storage**: Persists clean data into a structured SQL database for downstream querying.
*   **Observability**: Comprehensive logging of every pipeline step for monitoring and debugging.
*   **Modular Architecture**: Clean separation of concerns (Ingestion, Cleaning, Analysis, Reporting).

## Architecture

The system follows a standard Extract-Transform-Load (ETL) pattern:

1.  **Ingest**: The `DataIngestor` module validates and reads raw files.
2.  **Process**: The `DataCleaner` (planned) normalizes data structures.
3.  **Store**: The `DatabaseManager` handles transactional writing to SQLite/SQLAlchemy.
4.  **Analyze**: The `TrendAnalyzer` (planned) derives statistical insights.
5.  **Report**: The system generates human-readable artifacts (Markdown/PDF).

## Project Structure

*   `src/` - Core application logic libraries.
    *   `ingestion.py` - File handling and validation.
    *   `sql_utils.py` - Database connectivity and ORM.
    *   `logger.py` - Centralized logging configuration.
*   `data/` - Storage for raw input and processed output files.
*   `config/` - YAML-based configuration for paths and thresholds.
*   `main.py` - The orchestrator script that ties all modules together.

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Vichu2005g/data-pipeline-tool.git
    cd data-pipeline-tool
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  Place your raw data files (`.csv` or `.json`) in the `data/raw/` directory.
2.  Run the pipeline:
    ```bash
    python main.py
    ```
3.  Check the logs in `logs/pipeline.log` for execution details.

## Configuration

Edit `config/config.yaml` to adjust file paths, database locations, and analysis thresholds.

## CI/CD Service

This project includes an Azure DevOps pipeline configuration (`azure-pipelines.yml`) that automatically runs linting and integration tests on every commit, ensuring code quality and stability.