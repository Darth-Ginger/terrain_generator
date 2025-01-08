import logging
import sys
from loguru import logger
from functools import wraps
from datetime import datetime
from config import (
    LOGGING_LEVEL,
    ENABLE_TERMINAL_LOGGING,
    ENABLE_FILE_LOGGING,
    LOG_FILE_PATH,
    VERBOSE_LOGGING,
)

# InterceptHandler to route standard logging calls to Loguru
class InterceptHandler(logging.Handler):
    """Intercepts standard logging calls and routes them to Loguru."""

    def emit(self, record):
        level = logger.level(record.levelname).name if record.levelname in logger._core.levels else record.levelno
        logger.log(level, record.getMessage())


# Configure Loguru logger
logger.remove()  # Remove default logger

if ENABLE_TERMINAL_LOGGING:
    logger.add(
        sink=sys.stdout,
        level=LOGGING_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message} | <cyan>{name}</cyan>:<cyan>{function}</cyan>",
    )

if ENABLE_FILE_LOGGING:
    logger.add(
        sink=LOG_FILE_PATH,
        level="DEBUG",  # Always log INFO and above to the file
        rotation="10 MB",  # Rotate logs after reaching 10MB
        retention="7 days",  # Retain logs for 7 days
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message} | <cyan>{name}</cyan>:<cyan>{function}</cyan>",
        enqueue=True,
        serialize=False,
    )


class LoggerUtility:
    """Wrapper around Loguru for standardized logging and decorators."""

    @staticmethod
    def log_startup_header():
        """Logs a startup header to the terminal and/or log file."""
        header = "=" * 80
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        startup_message = f"{header}\n Script started at {timestamp}\n{header}"

        # Write the header to the terminal if enabled
        if ENABLE_TERMINAL_LOGGING:
            print(startup_message)

        # Write the header to the log file if enabled
        if ENABLE_FILE_LOGGING:
            with open(LOG_FILE_PATH, "a") as log_file:
                log_file.write(f"{startup_message}\n")
                
    @staticmethod
    def debug(message: str):
        logger.debug(message)

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def success(message: str):
        logger.success(message)

    @staticmethod
    def warning(message: str):
        logger.warning(message)

    @staticmethod
    def error(message: str):
        logger.error(message)

    @staticmethod
    def critical(message: str):
        logger.critical(message)

    @staticmethod
    def exception(message: str):
        logger.exception(message)

    @staticmethod
    def log_method(func):
        """Decorator to log method details (inputs, outputs, exceptions)."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"Entering: {func.__qualname__}:\n\t args:\n\t\t {args},\n\t kwargs:\n\t\t {kwargs}")

            try:
                result = func(*args, **kwargs)
                exec_time = f"{(datetime.now() - datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).total_seconds():.4f}s"

                # Log the result and execution time
                if VERBOSE_LOGGING:
                    logger.debug(
                        f"Exiting: {func.__qualname__}:\n\t Execution Time: {exec_time},\n\t Args:\n\t\t {args},\n\t Kwargs:\n\t\t {kwargs},\n\t Result: \n\t\t{result}"
                    )
                else:
                    logger.debug(
                        f"Exiting: {func.__qualname__}:\n\t Execution Time: {exec_time}"
                    )
                return result

            except Exception as e:
                # Log exceptions
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise

        return wrapper
