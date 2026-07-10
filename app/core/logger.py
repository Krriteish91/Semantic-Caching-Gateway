import logging
import sys


def setup_logger():

    logger = logging.getLogger("semantic_cache")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = setup_logger()