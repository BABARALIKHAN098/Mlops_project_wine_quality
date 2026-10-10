import os
import yaml
import json
import joblib

from os import PathLike
from pathlib import Path
from typing import Any

from ensure import ensure_annotations
from box import ConfigBox

from src.Mlops_project_quality_predictor.utils import logger


def read_yaml(path_to_yaml: str | PathLike[str]) -> ConfigBox:
    """
    Read a YAML configuration file and return its contents
    as a ConfigBox object.

    Args:
        path_to_yaml (str | PathLike[str]): Path to the YAML configuration file.

    Returns:
        ConfigBox: YAML file contents converted into a ConfigBox.

    Raises:
        FileNotFoundError: If the YAML file does not exist.
        ValueError: If the YAML is empty or has invalid syntax.
        TypeError: If the YAML document is not a mapping.
    """
    path = Path(path_to_yaml).expanduser()

    if not path.exists():
        message = f"YAML file does not exist: {path.resolve()}"
        logger.error(message)
        raise FileNotFoundError(message)

    if not path.is_file():
        message = f"YAML path is not a file: {path.resolve()}"
        logger.error(message)
        raise IsADirectoryError(message)

    resolved_path = path.resolve()

    try:
        raw_content = path.read_text(encoding="utf-8")
        content = yaml.safe_load(raw_content)
    except yaml.YAMLError as exc:
        logger.exception("Invalid YAML syntax in %s", resolved_path)
        raise ValueError(f"Invalid YAML syntax in {resolved_path}: {exc}") from exc

    if content is None:
        message = f"YAML file is empty or contains no mapping: {resolved_path}"
        logger.error(message)
        raise ValueError(message)

    if not isinstance(content, dict):
        message = (
            f"Expected a YAML mapping (dictionary) in {resolved_path}; "
            f"got {type(content).__name__}"
        )
        logger.error(message)
        raise TypeError(message)

    logger.info("YAML file loaded successfully: %s", resolved_path)
    return ConfigBox(content)


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
