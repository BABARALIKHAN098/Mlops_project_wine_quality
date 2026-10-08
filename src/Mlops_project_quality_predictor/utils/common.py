import os
import yaml
import json
import joblib

from pathlib import Path
from typing import Any

from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError

from src.Mlops_project_quality_predictor import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read a YAML configuration file and return its contents
    as a ConfigBox object.

    Args:
        path_to_yaml (Path): Path to the YAML configuration file.

    Returns:
        ConfigBox: YAML file contents converted into a ConfigBox.

    Raises:
        ValueError: If the YAML file is empty.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)

            logger.info(
                f"yaml file: {path_to_yaml} is loaded successfully"
            )

            return ConfigBox(content)

    except BoxValueError:
        raise ValueError("yaml file is empty")

    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """
    Create multiple directories if they do not already exist.

    Args:
        path_to_directories (list): List of directory paths to create.
        verbose (bool): If True, log a message after creating
                        each directory.

    Returns:
        None
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)

        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save a Python dictionary as a JSON file.

    Args:
        path (Path): Path where the JSON file will be saved.
        data (dict): Dictionary containing the data to save.

    Returns:
        None
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

        logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load a JSON file and convert its contents into a ConfigBox.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: JSON data converted into a ConfigBox object.
    """
    with open(path) as f:
        content = json.load(f)

        logger.info(
            f"json file loaded successfully from: {path}"
        )

        return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save any Python object as a binary file using Joblib.

    Args:
        data (Any): Python object that needs to be saved.
        path (Path): Path where the binary file will be stored.

    Returns:
        None
    """
    joblib.dump(value=data, filename=path)

    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load a Python object from a binary file using Joblib.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: The Python object loaded from the binary file.
    """
    data = joblib.load(path)

    logger.info(f"binary file loaded from: {path}")

    return data