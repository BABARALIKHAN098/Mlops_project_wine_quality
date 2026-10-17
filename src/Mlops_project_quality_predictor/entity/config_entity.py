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


@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Typed container for everything the ModelTrainer stage needs.
    Built by ConfigurationManager.get_model_trainer() and passed into ModelTrainer.
    """

    root_dir: Path          # Folder where the trained model will be saved
    train_data_path: Path   # Path to the training CSV
    test_data_path: Path    # Path to the test CSV
    model_name: str         # Filename of the saved model (e.g., model.joblib)
    alpha: float            # ElasticNet overall regularization strength
    l1_ratio: float         # ElasticNet mix of L1 (Lasso) vs L2 (Ridge) penalty
    target_column: str      # Name of the column the model should predict

@dataclass()
class ModelEvaluationConfig:
    """Holds all settings needed for the model evaluation stage."""

    root_dir: Path            # Root folder where evaluation outputs are stored
    test_data_path: Path      # Path to the test dataset (e.g., test.csv)
    model_path: Path          # Path to the trained model file (e.g., model.joblib)
    all_params: dict          # Model hyperparameters (e.g., from params.yaml)
    metric_file_name: Path    # File where evaluation metrics (e.g., JSON) are saved
    target_column: str        # Name of the target/label column in the dataset
    mlflow_uri: str           # MLflow tracking server URI for logging experiments        # MLflow tracking server URI for logging experiments
    



