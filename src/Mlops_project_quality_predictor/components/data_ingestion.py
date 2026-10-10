from src.Mlops_project_quality_predictor.config.configuration import *
import os
import urllib.request as request
from urllib.request import urlretrieve

from src.Mlops_project_quality_predictor.utils import logger
import zipfile


# Create a class to manage dataset downloading and extraction.
class DataIngestion:

    # Initialize the class with the data ingestion configuration.
    def __init__(self, config: DataIngestion_Config):
        # Store the configuration object for use in other methods.
        self.config = config

    # Download the dataset ZIP file if it does not already exist.
    def download_file(self):

        # Convert the configured file path to a Path object.
        local_data_file = Path(self.config.local_data_file)

        # Create the parent directory if it does not exist.
        local_data_file.parent.mkdir(parents=True, exist_ok=True)

        # Check whether the dataset file already exists.
        if not local_data_file.exists():

            # Download the file from the configured source URL.
            filename, headers = urlretrieve(
                url=self.config.source_url,
                filename=str(local_data_file)
            )

            # Log the downloaded filename and response headers.
            logger.info(
                f"{filename} downloaded with the following info:\n{headers}"
            )

        else:
            # Log that downloading is unnecessary.
            logger.info("File already exists.")

    # Extract the downloaded ZIP file into the configured directory.
    def extract_zip_file(self):

        # Convert the extraction directory to a Path object.
        unzip_path = Path(self.config.unzip_dir)

        # Create the extraction directory if it does not exist.
        unzip_path.mkdir(parents=True, exist_ok=True)

        # Open the downloaded ZIP archive in read mode.
        with zipfile.ZipFile(
            self.config.local_data_file, "r"
        ) as zip_ref:

            # Extract all archive contents into the target directory.
            zip_ref.extractall(unzip_path)

        # Log successful extraction.
        logger.info(f"Files extracted successfully to: {unzip_path}")

