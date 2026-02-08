import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Create a custom logger
logger = logging.getLogger("todo_backend")
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatters and add to handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)

# Also configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def log_info(message: str, extra: Dict[str, Any] = None):
    """Log an info message"""
    if extra:
        logger.info(message, extra=extra)
    else:
        logger.info(message)

def log_error(message: str, extra: Dict[str, Any] = None):
    """Log an error message"""
    if extra:
        logger.error(message, extra=extra)
    else:
        logger.error(message)

def log_warning(message: str, extra: Dict[str, Any] = None):
    """Log a warning message"""
    if extra:
        logger.warning(message, extra=extra)
    else:
        logger.warning(message)

def log_debug(message: str, extra: Dict[str, Any] = None):
    """Log a debug message"""
    if extra:
        logger.debug(message, extra=extra)
    else:
        logger.debug(message)