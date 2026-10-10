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
