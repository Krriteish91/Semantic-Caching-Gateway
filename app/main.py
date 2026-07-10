from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.middleware.exception_handler import register_exception_handlers

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

register_exception_handlers(app)
app.include_router(router)