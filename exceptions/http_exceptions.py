from interfaces.exception_repository import AppHTTPException


class NotFoundException(AppHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)


class AnotherPartException(AppHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
