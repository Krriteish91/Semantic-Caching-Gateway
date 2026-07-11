from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.middleware.exception_handler import register_exception_handlers
from app.middleware.request_id import request_id_middleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.middleware("http")(request_id_middleware)
register_exception_handlers(app)
app.include_router(router)