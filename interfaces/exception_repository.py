from fastapi import HTTPException


class AppHTTPException(HTTPException):
    """Базовое приложение для исключений"""
    pass
