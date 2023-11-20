import os
import logging

def create_logs(filename, type):
    """
    Create a log file and configure a logger.

    This function creates a log file in a 'logs' directory and configures a logger
    for writing log messages to this file.

    :param filename: The name of the log file (without the extension).
    :param type: The logger's name, typically representing the module or functionality being logged.
    :return: Configured logging.Logger object.
    """
    # Create the 'logs' directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create and configure the logger
    logger = logging.getLogger(type)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f'logs/{filename}.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Setting up a logger for search operations
execution_logger = create_logs('execution_log', 'search')
loading_logger = create_logs('loading_log', 'loading')
