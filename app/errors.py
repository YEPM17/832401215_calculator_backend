from fastapi import HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse


def install_exception_handlers(app) -> None:
    @app.exception_handler(HTTPException)
    async def http_error(request: Request, error: HTTPException):
        if isinstance(error.detail, dict):
            return JSONResponse(status_code=error.status_code, content=error.detail)
        return await http_exception_handler(request, error)

    @app.exception_handler(Exception)
    async def unhandled(_: Request, error: Exception):
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error"},
        )
