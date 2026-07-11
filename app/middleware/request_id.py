from uuid import uuid4
from app.core.logger import request_id_context
from fastapi import Request


async def request_id_middleware(
    request: Request,
    call_next,
):
    request_id = str(uuid4())

    request.state.request_id = request_id

    request_id_context.set(request_id)

    response = await call_next(request)

    response.headers["X-Request-ID"] = request.state.request_id

    return response