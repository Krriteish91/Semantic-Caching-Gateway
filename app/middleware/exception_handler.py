from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    SemanticCacheException,
)
from app.core.logger import logger
from app.core.metrics import REQUEST_FAILURES

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(SemanticCacheException)
    async def semantic_cache_exception_handler(
        request: Request,
        exc: SemanticCacheException,
    ):
        REQUEST_FAILURES.inc()
        logger.exception(str(exc))

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": str(exc),
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        REQUEST_FAILURES.inc()
        logger.exception(str(exc))

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred.",
                }
            },
        )