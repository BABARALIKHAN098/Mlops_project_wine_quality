# Project logger (imported from utils, same as in the other modules).
from src.Mlops_project_quality_predictor.utils import logger

# Pipeline stage classes. The module names must match your actual file names.
from src.Mlops_project_quality_predictor.pipeline.data_ingestion_pipline import DataIngestionTrainingPipeline
from src.Mlops_project_quality_predictor.pipeline.data_validation_pipline import DataValidationTrainingPipeline


# ---------------------------------------------------------------
# Stage 1: Data Ingestion (download the zip and extract the CSV)
# ---------------------------------------------------------------
STAGE_NAME = "DataIngestionStage"

try:
    # Log that the stage has started.
    logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<")

    # Create the ingestion pipeline object and run it.
    # (The method name must match the one defined in the ingestion pipeline class.)
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initial_data_ingestion()

    # Log successful completion.
    logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<\n\nx=======================x")

except Exception as e:
    # Save the full traceback to the log, then re-raise so the failure is not hidden.
    logger.exception(e)
    raise e


# ---------------------------------------------------------------
# Stage 2: Data Validation (check CSV columns against schema.yaml)
# ---------------------------------------------------------------
STAGE_NAME = "DATA_Validation_Stage"

try:
    # Log that the stage has started.
    logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<")

    # Create the validation pipeline object and run it.
    # This reads the config, loads the CSV, and writes True/False to the status file.
    data_validation = DataValidationTrainingPipeline()
    data_validation.initiate_data_validation()

    # Log successful completion.
    logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<\n\nx=======================x")

except Exception as e:
    # Save the full traceback to the log, then re-raise.
    logger.exception(e)
    raise e