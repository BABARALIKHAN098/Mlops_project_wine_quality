import os 
import pandas as pd
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
from src.Mlops_project_quality_predictor.config.configuration import ModelEvaluationConfig
import numpy as np
import joblib
from pathlib import Path
from src.Mlops_project_quality_predictor.utils.common import save_json
import json




class ModelEvaluation:
    """Evaluates the trained model on test data and logs results to MLflow."""

    def __init__(self, config: ModelEvaluationConfig):
        # Store the config so every method can access paths and params
        self.config = config

    def eval_metrics(self, actual, pred):
        """Return RMSE, MAE and R2 for the given actual and predicted values."""
        rmse = np.sqrt(mean_squared_error(actual, pred))  # Root mean squared error
        mae = mean_absolute_error(actual, pred)           # Mean absolute error
        r2 = r2_score(actual, pred)                       # Coefficient of determination
        return rmse, mae, r2

    def log_into_mlflow(self):
        """Load the model and test data, compute metrics, save them locally, and log to MLflow."""

        # Load the test dataset and the trained model
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        # Split features and target (columns=[...] is the safe way; axis=-1 is invalid)
        test_x = test_data.drop(columns=[self.config.target_column])
        test_y = test_data[self.config.target_column]

        # Point MLflow to the tracking server (a URL, not a token)
        mlflow.set_tracking_uri(self.config.mlflow_uri)

        # Find out if the tracking store is a local "file" store or a remote server
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Start a new MLflow run (the method is start_run, not start.run)
        with mlflow.start_run():
            # Predict on the test features
            predicted_qualities = model.predict(test_x)

            # Calculate evaluation metrics
            rmse, mae, r2 = self.eval_metrics(test_y, predicted_qualities)

            # Save metrics locally as JSON
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            # Log hyperparameters and metrics to MLflow
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2", r2)

            # The model registry does not work with a local file store,
            # so only register the model when using a remote server
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticNet")
            else:
                mlflow.sklearn.log_model(model, "model")