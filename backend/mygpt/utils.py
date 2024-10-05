import logging
import os
from datetime import datetime

def setup_logger():
    log_dir = os.path.join('logs')
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'run_{timestamp}.log')
    
    # Create a custom logger
    logger = logging.getLogger('backend')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    log_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)

    # # Configure root logger to use the same handler
    # root_logger = logging.getLogger()
    # root_logger.setLevel(logging.DEBUG)
    # root_logger.addHandler(file_handler)

    return logger, log_file

# Create a global logger instance
logger, log_file = setup_logger()