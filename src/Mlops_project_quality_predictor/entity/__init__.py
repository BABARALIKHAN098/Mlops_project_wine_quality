
import os
import sys
import logging

# Define the log message format.
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Define the directory where log files will be stored.
log_dir = "logs"

# Create the log directory if it does not exist.
os.makedirs(log_dir, exist_ok=True)

# Define the complete path of the log file.
log_file_path = os.path.join(log_dir, "running_logs.log")

# Configure logging to write messages to a file and the console.
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a reusable logger for the project.
logger = logging.getLogger("MlopsProjectLogger")
