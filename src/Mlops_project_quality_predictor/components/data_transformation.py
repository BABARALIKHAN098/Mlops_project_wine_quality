import os
from src.Mlops_project_quality_predictor.utils import logger
from  sklearn.model_selection import train_test_split
import pandas as pd
from src.Mlops_project_quality_predictor.config.configuration import ConfigurationManager
from src.Mlops_project_quality_predictor.config.configuration import DataTransformationConfig


class DataTransformation:
    """
    Handles the data transformation stage of the pipeline.
    Currently it only splits the dataset into train and test sets.
    """

    def __init__(self, config: DataTransformationConfig):
        # Store the config object (root_dir, data_path) built by ConfigurationManager
        self.config = config

    def train_test_splitting(self):
        """
        Read the raw dataset, split it into train/test sets,
        and save both as CSV files in the transformation folder.
        """

        # Load the input data from the path given in the config
        data = pd.read_csv(self.config.data_path)

        # Split into train and test sets
        # (sklearn default: 75% train / 25% test, shuffled, no fixed seed)
        train, test = train_test_split(data)

        # Save the training set; index=False avoids writing the row index as an extra column
        train.to_csv(os.path.join(self.config.root_dir, 'train.csv'), index=False)

        # Save the test set in the same folder
        test.to_csv(os.path.join(self.config.root_dir, 'test.csv'), index=False)

        # Log that the split completed and record the resulting shapes
        logger.info("Split data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        # Also print the shapes to the console for quick feedback
        print(train.shape)
        print(test.shape)
