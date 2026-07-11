import logging
import sys
from contextvars import ContextVar

request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)
class RequestIdFilter(logging.Filter):

    def filter(self, record):

        record.request_id = request_id_context.get()

        return True

def setup_logger():

    logger = logging.getLogger("semantic_cache")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | [%(request_id)s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)

    handler.addFilter(RequestIdFilter())

    logger.addHandler(handler)

    return logger


logger = setup_logger()