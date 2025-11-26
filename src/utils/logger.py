import logging
import sys
from datetime import datetime

# Configure logging format - simplified for status tracking
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with console handler.
    
    Args:
        name: Name of the logger (typically __name__)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    
    return logger

def log_step(logger: logging.Logger, step_name: str, status: str = "STARTED"):
    """
    Log the status of a step/agent.
    
    Args:
        logger: Logger instance
        step_name: Name of the step/agent
        status: Status (STARTED, COMPLETED, FAILED)
    """
    logger.info(f"[{status}] {step_name}")
