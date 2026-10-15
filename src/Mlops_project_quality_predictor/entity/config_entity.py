# Import the dataclass decorator to automatically generate methods
# such as __init__() and __repr__() for the class.
from dataclasses import dataclass

# Import Path to represent filesystem paths in a platform-independent way.
from pathlib import Path


# Convert this class into a dataclass for storing configuration data.
@dataclass
class DataIngestion_Config:

    # Store the root directory for the data ingestion process.
    root_dir: Path

    # Store the URL from which the dataset will be downloaded.
    source_url: str

    # Store the local filesystem path where the downloaded dataset will be saved.
    local_data_file: Path

    # Store the directory path where the downloaded dataset will be extracted.
    unzip_dir: Path

@dataclass
class DataValidationConfig:
    # Folder where validation outputs (e.g. the status file) are stored.
    # Comes from `data_validation.root_dir` in config.yaml.
    root_dir: Path

    # Path of the text file where the validation result (True/False) is written.
    # Comes from `data_validation.STATUS_FILE` in config.yaml.
    STATUS_FILE: str

    # Path to the CSV file that will be validated
    # (here: artifacts/data_ingestion/winequality-red.csv).
    # Comes from `data_validation.unzip_data_dir` in config.yaml.
    unzip_data_dir: Path

    # Expected schema: a dictionary of column names and their data types
    # (e.g. {"alcohol": "float64", ...}).
    # Comes from the `COLUMNS` section of schema.yaml.
    # The validator checks that every column in the CSV exists in this dict.
    all_schema: dict





@dataclass
class DataTransformationConfig:
    root_dir : Path
    data_path : Path



