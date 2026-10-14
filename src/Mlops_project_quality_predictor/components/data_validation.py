import os
import pandas as pd

# Project logger for recording validation results.
from src.Mlops_project_quality_predictor.utils import logger

# Dataclass holding the paths and schema needed for validation.
from src.Mlops_project_quality_predictor.entity.config_entity import DataValidationConfig


# Class name fixed: "DataValiadtion" -> "DataValidation".
class DataValidation:
    """Checks that the dataset columns match the columns defined in schema.yaml."""

    def __init__(self, config: DataValidationConfig):
        # Store the config (CSV path, status file path, expected schema).
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            # Load the dataset that needs to be validated.
            data = pd.read_csv(self.config.unzip_data_dir)

            # Column names found in the CSV.
            all_cols = list(data.columns)

            # Column names expected by the schema (keys of the COLUMNS section).
            all_schema = self.config.all_schema.keys()

            # Collect every CSV column that is NOT in the schema.
            # (The old loop overwrote the status on each column, so only the
            # last column decided the result. Collecting them first fixes that.)
            invalid_cols = [col for col in all_cols if col not in all_schema]

            # Valid only if there are no unexpected columns.
            validation_status = len(invalid_cols) == 0

            # Write the final result once, after all columns are checked.
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")

            # Log which columns failed, to make debugging easier.
            if not validation_status:
                logger.warning(f"Columns not found in schema: {invalid_cols}")

            return validation_status

        except Exception as e:
            # Re-raise so the pipeline stage can log the failure.
            raise e