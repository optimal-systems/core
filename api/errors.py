import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

_LOG = logging.getLogger(__name__)


def register_handlers(app):
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception):
        _LOG.exception("Unhandled error")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error", "detail": str(exc)}
        )
