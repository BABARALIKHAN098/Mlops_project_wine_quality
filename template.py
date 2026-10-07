import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s:'
)

project_name = "Mlops_project_quality_predictor"

list_of_files = [
    ".github/workflows/.gitkeep",

    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",

    "config/config.yaml",
    "params.yaml",
    "main.py",
    "Dockerfile",
    "setup.py",
    "research/research.ipynb",
    "template/index.html"
    "README.md",
    "requirements.txt",
    ".gitignore"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    filedir = filepath.parent
    filename = filepath.name

    # Create directory only if there is a directory component
    if filedir != Path("."):
        filedir.mkdir(parents=True, exist_ok=True)

    logging.info(
        f"Creating directory {filedir} for the file: {filename}"
    )

    # Create file if it doesn't exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")