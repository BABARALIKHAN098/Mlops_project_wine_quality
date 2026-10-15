from src.Mlops_project_quality_predictor.config.configuration import ConfigurationManager
from src.Mlops_project_quality_predictor.components.data_transformation import DataTransformation
from pathlib import Path
from src.Mlops_project_quality_predictor.utils import logger


STAGE_NAME = "Data_Transformation_Stage"


class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        # BUG FIX: the status check used to sit in the class body, so it ran
        # once at import time. It must live inside a method so it runs
        # each time the pipeline is executed.
        try:
            # BUG FIX: 'r' was passed to Path() instead of open().
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                # BUG FIX: strip() removes trailing newline/spaces that would
                # make the comparison with "True" fail.
                # status.txt looks like "Validation status: True"
                status = f.read().strip().split(" ")[-1]

            if status == "True":
                config = ConfigurationManager()
                # BUG FIX: was get_data_ingestion_config(); transformation
                # needs its own config.
                data_transformation_config = config.get_data_transformation_config()

                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_splitting()
            else:
                # Schema validation failed in the previous stage, so stop here.
                raise Exception("Your data schema is not valid")

        except Exception as e:
            # BUG FIX: print(e) swallowed the error and let the pipeline look
            # successful. Log it and re-raise so the failure is visible.
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e


                  