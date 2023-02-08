from typing import Optional, List

from typing_extensions import TypedDict


class Error(TypedDict):
    code: str
    message: str
    fieldPaths: Optional[List[str]]


class Status(TypedDict):
    code: int
    message: str


class Response(TypedDict):
    status: Status
    errors: Optional[List[Error]]
    count: int


class Request(TypedDict):
    id: str
    url: str
    method: str
    timestamp: str


class ApiResponse(TypedDict):
    request: Request
    response: Response
