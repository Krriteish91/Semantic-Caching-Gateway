from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.middleware.exception_handler import register_exception_handlers
from app.middleware.request_id import request_id_middleware
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest

from fastapi import Response


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.middleware("http")(request_id_middleware)
register_exception_handlers(app)
app.include_router(router)

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )