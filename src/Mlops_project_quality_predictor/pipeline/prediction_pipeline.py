import joblib
import numpy as np
import pandas as pd
from pathlib import Path


class PredictionPipeline:
    """Loads a trained model and uses it to make predictions."""

    def __init__(self):
        # Build the path relative to the project root, not the working directory,
        # so it works no matter where the script is run from.
        # Adjust parents[n] to match where this file sits in your project.
        model_path = Path(__file__).resolve().parents[3] / "artifacts" / "model_trainer" / "model.joblib"

        # Fail early with a clear message if the model file is missing
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        # Load the trained model saved by the training stage
        self.model = joblib.load(model_path)

    def predict(self, data):
        """
        Make predictions on the input data.

        Args:
            data: DataFrame, 2D array, or list of lists with the same
                  features (and order) used during training.

        Returns:
            numpy array of predictions.
        """
        # Convert lists/arrays to a DataFrame, and make sure the input is 2D
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(np.atleast_2d(data))

        # FIX: the method is `predict`, not `prediction`
        prediction = self.model.predict(data)

        return prediction