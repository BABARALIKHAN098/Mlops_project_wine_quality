from src.Mlops_project_quality_predictor.entity import logger
from src.Mlops_project_quality_predictor.pipeline.data_ingestion_pipline import DataIngestionTrainingPipeline


STAGE_NAME="DataIngestionStage"

try:
    logger.info(f" Stage {STAGE_NAME} started")

    data_ingestion=DataIngestionTrainingPipeline()
    data_ingestion.initial_data_ingestion()

    logger.info(f"stage {STAGE_NAME},completed")

except Exception as e:
    logger.exception(e)
    raise e