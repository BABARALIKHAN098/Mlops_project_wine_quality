# Project logger (imported from utils, same as in the other modules).
from src.Mlops_project_quality_predictor.utils import logger

# Pipeline stage classes. The module names must match your actual file names.
from src.Mlops_project_quality_predictor.pipeline.data_ingestion_pipline import DataIngestionTrainingPipeline
from src.Mlops_project_quality_predictor.pipeline.data_validation_pipline import DataValidationTrainingPipeline
from src.Mlops_project_quality_predictor.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.Mlops_project_quality_predictor.pipeline.model_trainer_pipeline import ModelTrainerTrainingpipeline
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


STAGE_NAME = "Data_Transformation_Stage"

# BUG FIX: without this guard, the stage would also run on import
# (for example from a test or another module), not just when executed directly.
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")

        # STYLE FIX: lowercase variable name.
        data_transformation = DataTransformationPipeline()

        # NOTE: this method name must match the one defined in the class.
        # Your original class had initiate_data_ingestion(), so either
        # rename it there or call that name here.
        data_transformation.initiate_data_transformation()

        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        # Log the full traceback, then re-raise so the failure isn't hidden
        # and the pipeline (or DVC/CI) stops with a non-zero exit code.
        logger.exception(e)
        raise



# Name of this stage, used in the log messages
STAGE_NAME = "Model_trainer_STAGE"

try:
    # Log the start of the stage so it's easy to find in the log file
    logger.info(f">>>>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<<<<")

    # Create the pipeline object for the model training stage
    model_trainer_pipeline = ModelTrainerTrainingpipeline()

    # Run the stage: build config -> create trainer -> train and save the model
    model_trainer_pipeline.initiate_model_training()

    # Log successful completion, followed by a separator line for readability
    logger.info(f">>>>>>>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<\n\nx==================x")

except Exception as e:
    # Log the full traceback so the failure is recorded in the log file
    logger.exception(e)

    # Re-raise so the pipeline stops instead of silently continuing
    raise e