from src.Mlops_project_quality_predictor.config.configuration import ConfigurationManager
from src.Mlops_project_quality_predictor.components.Model_trainer import ModelTrainer
from src.Mlops_project_quality_predictor.utils import logger


# Name of this pipeline stage, used in log messages
STAGE_NAME = "Model_Trainer_stage"


class ModelTrainerTrainingpipeline:
    """Runs the model training stage: build config -> create trainer -> train."""

    def __init__(self):
        # No setup needed, the stage is configured in initiate_model_training()
        pass

    def initiate_model_training(self):
        # Load config.yaml, params.yaml and schema.yaml
        config = ConfigurationManager()

        # Build the typed config object for the model trainer stage
        model_trainer_config = config.get_model_trainer()

        # Create the trainer with that config (separate name, so the config isn't overwritten)
        model_trainer = ModelTrainer(config=model_trainer_config)

        # Load the data, train the ElasticNet model, and save it to disk
        model_trainer.train()


# Run this stage directly (e.g., `python this_file.py`) with logging and error handling
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ModelTrainerTrainingpipeline()
        pipeline.initiate_model_training()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        # Log the full traceback, then re-raise so the pipeline stops
        logger.exception(e)
        raise e