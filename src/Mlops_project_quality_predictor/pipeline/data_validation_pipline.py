# Manager that reads config.yaml / params.yaml / schema.yaml and builds config objects.
from src.Mlops_project_quality_predictor.config.configuration import ConfigurationManager

# The component class that does the actual validation work.
# (Match the spelling used in your component file: DataValidation or DataValiadtion.)
from src.Mlops_project_quality_predictor.components.data_validation import DataValidation

# Project logger used to record when the stage starts, finishes or fails.
from src.Mlops_project_quality_predictor.utils import logger


# Name of this pipeline stage, used in the log messages.
STAGE_NAME = "DATA_Validation_stage"


class DataValidationTrainingPipeline:
    """Pipeline stage that checks the dataset columns against the expected schema."""

    def __init__(self):
        # No setup needed; all work happens in initiate_data_validation().
        pass

    def initiate_data_validation(self):
        # Load the configuration files through the ConfigurationManager.
        config = ConfigurationManager()

        # Build the DataValidationConfig object (paths + schema) from the YAML values.
        data_validation_config = config.get_data_validation_config()

        # Create the validation component with that config.
        data_validation = DataValidation(config=data_validation_config)

        # Run the validation. It compares the CSV columns with the schema
        # and writes True/False to the status file.
        data_validation.validate_all_columns()


# This block runs only when the file is executed directly (python this_file.py),
# not when it is imported by another module.
if __name__ == "__main__":
    try:
        # Log that the stage has started.
        logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<<<")

        # Create the pipeline object and run the stage.
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()

        # Log successful completion.
        logger.info(f">>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        # Write the full traceback to the log, then re-raise so the failure is visible.
        logger.exception(e)
        raise e