import os
import functools
import pathlib
import sys
import yaml
import logging
import logging.config


# Set PythonPath if not done in Terminal
root_dir = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(root_dir)

# create logger
logging.config.fileConfig(root_dir / "logging.conf")
logger = logging.getLogger(__name__)

env = os.getenv("ENV", "dev")
match env:
    case "dev" | "staging" | "prod":
        pass
    case _:
        raise EnvironmentError(f"Wrong environment variable: ENV={env}")

# Fetch App Config
with open(root_dir / f"config/{env}.yaml") as f:
    app_config = yaml.safe_load(f)


def wrap_log(func):
    """Use as Decorator to add Function level Logging"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"Started function {func.__name__}")
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Completed function {func.__name__}")
            return result
        except Exception as exp:
            logger.info(f"Aborted function {func.__name__}")
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(exp)}")
            raise exp

    return wrapper
