# Dataclasses that hold the settings for each pipeline stage.
from src.Mlops_project_quality_predictor.entity.config_entity import (
    DataIngestion_Config,
    DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig   # NEW: needed by get_data_validation_config()
)

# Paths to config.yaml, params.yaml and schema.yaml.
from src.Mlops_project_quality_predictor.constants import *
import os

# Helpers to read YAML files and create folders.
from src.Mlops_project_quality_predictor.utils.common import read_yaml, create_directories

import os
from dotenv import load_dotenv, find_dotenv  # Reads KEY=VALUE lines from .env into os.environ

# find_dotenv() searches the current folder and parent folders for a file named .env
# override=True replaces any old values that are already set in the environment
load_dotenv(find_dotenv(), override=True)

# Quick check (never print the token itself)
print(os.getenv("MLFLOW_TRACKING_URI"))       # Should print the .mlflow URL
print(os.getenv("MLFLOW_TRACKING_USERNAME"))  # Should print your username
print("Token set:", bool(os.getenv("MLFLOW_TRACKING_PASSWORD")))

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

    def get_data_transformation_config(self) -> DataTransformationConfig:
            """Build and return the config for the data transformation stage."""
    
            # Pull the data_transformation section out of config.yaml
            config = self.config.data_transformation
    
            # Create the folder where transformation outputs will be saved
            create_directories([config.root_dir])
    
            # Wrap the values in a dataclass so the next stage gets a typed object
            data_transformation_config = DataTransformationConfig(
                root_dir=config.root_dir,
                data_path=config.data_path
            )
    
            # Return it (without this line the method returns None)
            return data_transformation_config


    def get_model_trainer(self) -> ModelTrainerConfig:
                """
                Build and return the ModelTrainerConfig used by the ModelTrainer stage.
                Combines paths from config.yaml, hyperparameters from params.yaml,
                and the target column name from schema.yaml.
                """
                # Section of config.yaml with paths for the model trainer stage
                config = self.config.model_trainer
    
                # ElasticNet hyperparameters (alpha, l1_ratio) from params.yaml
                params = self.params.ElasticNet
    
                # Target column definition from schema.yaml
                schema = self.schema.TARGET
    
                # Create the model trainer's output directory if it doesn't exist
                create_directories([config.root_dir])
    
                # Bundle everything into a typed config object
                model_trainer_config = ModelTrainerConfig(
                    root_dir=config.root_dir,                  # Where the trained model will be saved
                    train_data_path=config.train_data_path,    # Path to the training CSV
                    test_data_path=config.test_data_path,      # Path to the test CSV
                    model_name=config.model_name,              # Filename for the saved model (e.g., model.joblib)
                    alpha=params.alpha,                        # Regularization strength
                    l1_ratio=params.l1_ratio,                  # L1 vs L2 penalty mix
                    target_column=schema.name,                 # Name of the column to predict
                )
    
                return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
            """Build and return the config object for the model evaluation stage."""
    
            config = self.config.model_evaluation   # Paths/files for this stage (config.yaml)
            params = self.params.ElasticNet         # Model hyperparameters (params.yaml)
            schema = self.schema.TARGET             # Target column info (schema.yaml)
    
            # Read the tracking URI from the environment (loaded from .env via load_dotenv).
            # It must be the DagsHub URL ending in .mlflow, never the token.
            mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
            if not mlflow_uri or not mlflow_uri.startswith("http"):
                raise ValueError(
                    "MLFLOW_TRACKING_URI is missing or is not a URL. "
                    "Run load_dotenv() before creating the config."
                )
    
            # Create the evaluation output folder if it doesn't exist yet
            create_directories([config.root_dir])
    
            model_evaluation_config = ModelEvaluationConfig(
                root_dir=Path(config.root_dir),                    # Folder for evaluation outputs
                test_data_path=Path(config.test_data_path),        # Test dataset location
                model_path=Path(config.model_path),                # Trained model location
                all_params=params,                                 # Hyperparameters to log
                metric_file_name=Path(config.metric_file_name),    # File where metrics are saved
                target_column=schema.name,                         # Name of the label column
                mlflow_uri=mlflow_uri,                             # DagsHub MLflow URL from the environment
            )
    
            return model_evaluation_config


    



    