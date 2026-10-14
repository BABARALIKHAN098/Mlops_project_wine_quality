# Dataclasses that hold the settings for each pipeline stage.
from src.Mlops_project_quality_predictor.entity.config_entity import (
    DataIngestion_Config,
    DataValidationConfig,   # NEW: needed by get_data_validation_config()
)

# Paths to config.yaml, params.yaml and schema.yaml.
from src.Mlops_project_quality_predictor.constants import *

# Helpers to read YAML files and create folders.
from src.Mlops_project_quality_predictor.utils.common import read_yaml, create_directories


# Class responsible for managing project configurations.
class ConfigurationManager:

    # Initialize the configuration manager with paths to configuration files.
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,   # Default path to the main config YAML file.
        params_filepath=PARAMS_FILE_PATH,   # Default path to the parameters YAML file.
        schema_filepath=SCHEMA_FILE_PATH,   # Default path to the schema YAML file.
    ):
        # Read the main YAML file and store its contents as a ConfigBox object.
        self.config = read_yaml(config_filepath)

        # Read the parameters YAML file and store its contents.
        self.params = read_yaml(params_filepath)

        # Read the schema YAML file and store its contents.
        self.schema = read_yaml(schema_filepath)

        # Create the main artifacts directory defined in the config file.
        create_directories([self.config.artifacts_root])

    # Build and return the configuration object for the data ingestion step.
    def get_data_ingestion_config(self) -> DataIngestion_Config:
        """
        Reads the `data_ingestion` section of config.yaml and packs those values
        into a DataIngestion_Config dataclass, so the ingestion component never
        has to touch the YAML file directly.
        """

        # Get the `data_ingestion` section from config.yaml (case-sensitive key).
        config = self.config.data_ingestion

        # Create artifacts/data_ingestion if it doesn't exist yet.
        create_directories([config.root_dir])

        # Build the config object from the YAML values.
        data_ingestion_config = DataIngestion_Config(
            root_dir=config.root_dir,                 # Folder for all ingestion outputs.
            source_url=config.source_url,             # URL the zip file is downloaded from.
            local_data_file=config.local_data_file,   # Where the downloaded zip is saved.
            unzip_dir=config.unzip_dir,               # Folder the zip is extracted into.
        )

        # Return the finished config object to the pipeline stage.
        return data_ingestion_config

    # NEW: build and return the configuration object for the data validation step.
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Reads the `data_validation` section of config.yaml and the COLUMNS
        section of schema.yaml, and packs them into a DataValidationConfig.
        """

        # Get the `data_validation` section from config.yaml (lowercase key).
        config = self.config.data_validation

        # Get the expected columns and types from the COLUMNS section of schema.yaml.
        schema = self.schema.COLUMNS

        # Create artifacts/data_validation if it doesn't exist yet,
        # so the status file can be written there.
        create_directories([config.root_dir])

        # Build the config object from the YAML values.
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,               # Folder for validation outputs.
            STATUS_FILE=config.STATUS_FILE,         # File where True/False is written.
            unzip_data_dir=config.unzip_data_dir,   # CSV file that will be validated.
            all_schema=schema,                      # Expected columns from schema.yaml.
        )

        # Return the finished config object to the pipeline stage.
        return data_validation_config