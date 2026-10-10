from src.Mlops_project_quality_predictor.entity.config_entity import DataIngestion_Config
	
from src.Mlops_project_quality_predictor.constants import *
from src.Mlops_project_quality_predictor.utils.common import read_yaml,create_directories




# Define a class responsible for managing project configurations.
class ConfigurationManager:

    # Initialize the configuration manager with paths to configuration files.
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,  # Set the default path to the main configuration YAML file.
        params_filepath=PARAMS_FILE_PATH,  # Set the default path to the parameters YAML file.
        schema_filepath=SCHEMA_FILE_PATH,  # Set the default path to the schema YAML file.
    ):
        # Read the main YAML file and store its contents as a ConfigBox object.
        self.config = read_yaml(config_filepath)

        # Read the parameters YAML file and store its contents.
        self.params = read_yaml(params_filepath)

        # Read the schema YAML file and store its contents.
        self.schema = read_yaml(schema_filepath)

        # Create the main artifacts directory defined in the configuration file.
        create_directories([self.config.artifacts_root])

    # Define a method that returns the data ingestion configuration object.
    def get_data_ingestion_config(self) -> DataIngestion_Config:

        # Access the data ingestion section of the main configuration.
        config = self.config.data_ingestion

        # Create the root directory required for the data ingestion pipeline.
        create_directories([config.root_dir])

        # Create a DataIngestion_Config object using values from the YAML file.
        data_ingestion_config = DataIngestion_Config(

            # Set the root directory for data ingestion.
            root_dir=config.root_dir,

            # Set the URL from which the dataset will be downloaded.
            source_url=config.source_url,

            # Set the local path where the downloaded dataset will be stored.
            local_data_file=config.local_data_file,

            # Set the directory where the downloaded dataset will be extracted.
            unzip_dir=config.unzip_dir,
        )

        # Return the completed data ingestion configuration object.
        return data_ingestion_config
