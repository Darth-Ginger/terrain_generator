import logging
import sys
from loguru import logger
from functools import wraps
import inspect
import time
from datetime import datetime
from config import LOGGING_LEVEL, ENABLE_TERMINAL_LOGGING, ENABLE_FILE_LOGGING, LOG_FILE_PATH, DEBUG_OUTPUT_FILE

# InterceptHandler to route standard logging to Loguru
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
        level="INFO",  # Log INFO, SUCCESS, and higher levels
        rotation="1 MB",  # Rotate logs after 1MB
        retention="7 days",  # Retain logs for 7 days
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message} | <cyan>{name}</cyan>:<cyan>{function}</cyan>",
    )

class LoggerUtility:
    """Wrapper around Loguru for standardized logging."""

    @staticmethod
    def debug(message: str):
        logger.debug(message)

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def success(message: str):
        logger.log("SUCCESS", message)

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
    def log_method_stats(func):
        """Logs method input, output, and execution time."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.debug(f"Entering: {func.__name__}, args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                exec_time = time.time() - start_time
                logger.info(f"Exiting: {func.__name__}, result: {result}, exec_time: {exec_time:.4f}s")
                return result
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise

        return wrapper

    @staticmethod
    def write_debug_output(file_path: str = DEBUG_OUTPUT_FILE):
        """Logs method output and trace in debug mode."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if logger.level("DEBUG").no > logger.level().no:
                    # If current logging level is not DEBUG, skip logging
                    return func(*args, **kwargs)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                caller = inspect.stack()[1]
                caller_info = f"File: {caller.filename}, Line: {caller.lineno}, Method: {caller.function}"
                method_name = func.__name__

                try:
                    # Log method call details
                    logger.debug(f"Entering: {method_name}, args: {args}, kwargs: {kwargs}")

                    # Execute the method and capture its output
                    result = func(*args, **kwargs)

                    # Prepare output to be written
                    output = (
                        f"[{timestamp}] Method: {method_name}\n"
                        f"Caller: {caller_info}\n"
                        f"Args: {args}\n"
                        f"Kwargs: {kwargs}\n"
                        f"Output: {result if result is not None else 'Method executed successfully with no return value.'}\n"
                    )

                    # Write to the debug file
                    with open(file_path, "a") as debug_file:
                        debug_file.write(output + "\n")

                    return result

                except Exception as e:
                    # Log and write any exceptions to the debug file
                    error_output = (
                        f"[{timestamp}] Method: {method_name}\n"
                        f"Caller: {caller_info}\n"
                        f"Args: {args}\n"
                        f"Kwargs: {kwargs}\n"
                        f"Exception: {e}\n"
                    )
                    with open(file_path, "a") as debug_file:
                        debug_file.write(error_output + "\n")

                    logger.exception(f"Exception in {method_name}: {e}")
                    raise

            return wrapper

        return decorator
