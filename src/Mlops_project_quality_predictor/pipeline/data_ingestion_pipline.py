
from src.Mlops_project_quality_predictor.config.configuration import ConfigurationManager
from src.Mlops_project_quality_predictor.components.data_ingestion import DataIngestion
from src.Mlops_project_quality_predictor.entity import logger


# Define the name of the pipeline stage.
STAGE_NAME = "Data Ingestion Stage"


# Create a pipeline class for data ingestion.
class DataIngestionTrainingPipeline:

    # Initialize the pipeline.
    def __init__(self):
        pass

    # Configure, download, and extract the dataset.
    def initial_data_ingestion(self):
        # Initialize the configuration manager.
        config = ConfigurationManager()

        # Load the data ingestion configuration.
        data_ingestion_config = config.get_data_ingestion_config()

        # Create the data ingestion component.
        data_ingestion = DataIngestion(data_ingestion_config)

        # Download the dataset.
        data_ingestion.download_file()

        # Extract the downloaded ZIP file.
        data_ingestion.extract_zip_file()

    # Provide a main method to run the pipeline.
    def main(self):
        self.initial_data_ingestion()


# Run the pipeline when this file is executed directly.
if __name__ == "__main__":

    try:
        # Log the start of the pipeline stage.
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")

        # Create the pipeline object.
        obj = DataIngestionTrainingPipeline()

        # Execute the pipeline.
        obj.main()

        # Log successful completion.
        logger.info(
            f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n"
            "X==============X"
        )

    except Exception:
        # Log the full exception traceback.
        logger.exception(f"Stage {STAGE_NAME} failed.")
        raise
