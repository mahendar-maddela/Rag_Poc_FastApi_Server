from typing import Optional, Any, Dict
from fastapi.responses import JSONResponse


def success_response(
    message: str,
    data: Optional[Dict[str, Any]] = None,
    status_code: int = 200,
    pagination: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    response_content = {
        "status": "success",
        "message": message,
    }
    if data is not None:
        response_content["data"] = data
    if pagination is not None:
        response_content["pagination"] = pagination

    return JSONResponse(status_code=status_code, content=response_content)


def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code, content={"status": "error", "message": message}
    )
