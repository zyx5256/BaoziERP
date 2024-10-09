import logging
import inspect
from functools import wraps


class DynamicLogFilter(logging.Filter):
    def filter(self, record):
        # Check if the logger was called from within the wrapper function
        if record.funcName == 'wrapper':
            # Get the stack frame of the actual caller (3 frames back, because we're inside the decorator)
            i = 0
            for frame_info in inspect.stack():
                if frame_info.function != 'wrapper':
                    i = i + 1
                    continue
                else:
                    break

            record.filename = inspect.stack()[i + 1].filename.split('/')[-1]
            record.funcName = inspect.stack()[i + 1].function
            record.lineno = inspect.stack()[i + 1].lineno
        return True


logger = logging.getLogger('erp_logger')
logger.setLevel(logging.DEBUG)

# Create file and console handlers
file_handler = logging.FileHandler('erp.log')
console_handler = logging.StreamHandler()

# Set log levels for handlers
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
formatter = logging.Formatter(
    "[%(asctime)s][%(levelname)-5s][%(process)d:%(thread)d][%(filename)s:%(lineno)d][%(funcName)s]: %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# Add the custom filter to the logger
log_filter = DynamicLogFilter()
logger.addFilter(log_filter)

def func_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"-> {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"<- {func.__name__}")
        return result
    return wrapper

