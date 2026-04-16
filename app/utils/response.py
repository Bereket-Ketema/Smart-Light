from typing import Any, Optional


def success_response(message: str, data: Optional[Any] = None, status_code: int = 200):
    return {
        "success": True,
        "message": message,
        "data": data,
        "error": None,
    }, status_code


def error_response(message: str, status_code: int = 400, error: Optional[Any] = None):
    return {
        "success": False,
        "message": message,
        "data": None,
        "error": error,
    }, status_code
