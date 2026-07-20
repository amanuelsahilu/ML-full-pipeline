import logging
import os
from datetime import datetime


def create_logger_file():
    log_folder = datetime.now().strftime("%Y_%m_%d")
    log_file = datetime.now().strftime("%H-%M-%S") + ".log"

    logs_path = os.path.join(os.getcwd(), "logs", log_folder)
    os.makedirs(logs_path, exist_ok=True)

    return os.path.join(logs_path, log_file)


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Prevent duplicate logs if this module is imported multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Log to file
    file_handler = logging.FileHandler(create_logger_file())
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Log to terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    logger.info("Testing the logger")