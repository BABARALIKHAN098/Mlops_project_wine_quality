from  src.Mlops_project_quality_predictor.config.configuration import ModelTrainerConfig
import pandas as pd
import os
from src.Mlops_project_quality_predictor.utils import logger
from sklearn.linear_model import ElasticNet
import joblib

class ModelTrainer:
    """Trains an ElasticNet regression model and saves it to disk."""

    def __init__(self, config: ModelTrainerConfig):
        # Store the config (data paths, hyperparameters, output location)
        self.config = config

    def train(self):
        # Load the training and test datasets from CSV files
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        # Split training data into features (X) and target (y)
        train_x = train_data.drop([self.config.target_column], axis=1)
        train_y = train_data[self.config.target_column]

        # Split test data the same way
        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[self.config.target_column]

        # Create the ElasticNet model using hyperparameters from the config
        # alpha    -> overall regularization strength
        # l1_ratio -> mix of L1 (Lasso) vs L2 (Ridge) penalty
        # random_state -> makes results reproducible
        lr = ElasticNet(
            alpha=self.config.alpha,
            l1_ratio=self.config.l1_ratio,
            random_state=42,
        )

        # Fit the model on the training data
        lr.fit(train_x, train_y)

        # Save the trained model to disk so it can be reused later
        joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))