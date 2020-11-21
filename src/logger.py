"""Module for logging messages"""
import logging
import sys

CONSOLE_FORMATTER = logging.Formatter("%(name)s - line %(lineno)d - %(message)s")
FILE_FORMATTER = logging.Formatter("%(asctime)s - %(name)s - line %(lineno)d - " \
                                   "%(levelname)s - %(message)s")

LOG_FILE = "debug.log"

# Open and close to clear the log
open(r'debug.log', 'w').close()

def get_console_handler():
    """Gets the handler for logs to the console"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    console_handler.setLevel(logging.CRITICAL)
    return console_handler

def get_file_handler():
    """Gets the handler for logs to the log file"""
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FILE_FORMATTER)
    return file_handler

def get_logger(logger_name):
    """Obtains new logger object made with the given name

    :param str logger_name: Name of the logger to be made
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
