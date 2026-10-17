# Component class that evaluates the model and logs results to MLflow
# (check the file name: "model_evauation" must match your actual file name exactly)
from src.Mlops_project_quality_predictor.components.model_evauation import ModelEvaluation

# Not used in this file, so it can be removed
from src.Mlops_project_quality_predictor.entity.config_entity import ModelEvaluationConfig

# Loads config.yaml, params.yaml and schema.yaml and builds the config objects
from src.Mlops_project_quality_predictor.config.configuration import ConfigurationManager

# Name of this pipeline stage (useful for logging, e.g., "stage started/completed")
STAGE_NAME = "Model evaluation stage"


class ModelEvaluationTrainingPipeline:
    """Runs the model evaluation stage of the pipeline."""

    def __init__(self):
        # No setup needed; everything is created inside the method below
        pass

    # Method name has a typo ("evaltion"). If you rename it, update main.py too.
    def initiate_model_evaltion(self):
        """Load config, evaluate the trained model, and log results to MLflow."""

        # Read the YAML files and create the configuration manager
        config = ConfigurationManager()

        # Build the typed config object for the model evaluation stage
        model_evaluation_config = config.get_model_evaluation_config()

        # Create the evaluator, passing it the config object
        # (fixed: was `model_evaluation+config`, which is invalid)
        model_evaluation = ModelEvaluation(config=model_evaluation_config)

        # Compute metrics, save them as JSON, and log params/metrics/model to MLflow
        model_evaluation.log_into_mlflow()