"""RFC 9457 problem details, the error format for every API response."""

from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

from pydantic import BaseModel
from starlette.responses import JSONResponse

PROBLEM_MEDIA_TYPE = "application/problem+json"


class Problem(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None


def status_phrase(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Error"


def problem_response(
    status_code: int,
    *,
    detail: str | None = None,
    instance: str | None = None,
    extensions: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    problem = Problem(
        title=status_phrase(status_code),
        status=status_code,
        detail=detail,
        instance=instance,
    )
    body = problem.model_dump(exclude_none=True) | dict(extensions or {})
    return JSONResponse(
        body,
        status_code=status_code,
        media_type=PROBLEM_MEDIA_TYPE,
        headers=headers,
    )
