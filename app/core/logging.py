"""Logging configuration.

Local development gets readable lines. Deployed environments emit one JSON object per line, which
Cloud Logging parses into structured entries (``severity`` and ``message`` are recognized fields).
"""

import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

_STANDARD_RECORD_ATTRS = frozenset(
    vars(logging.LogRecord("", logging.INFO, "", 0, "", None, None))
) | {"message", "asctime", "request_id"}

_UVICORN_LOGGERS = ("uvicorn", "uvicorn.error", "uvicorn.access")


class JsonFormatter(logging.Formatter):
    """Formats records as single-line JSON, including any ``extra={...}`` fields."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "time": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "logger": record.name,
        }
        request_id = request_id_var.get()
        if request_id is not None:
            payload["request_id"] = request_id
        payload.update(
            {key: value for key, value in vars(record).items() if key not in _STANDARD_RECORD_ATTRS}
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


class RequestIdFilter(logging.Filter):
    """Exposes the current request ID to text formatters as ``%(request_id)s``."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.__dict__["request_id"] = request_id_var.get() or "-"
        return True


def configure_logging(level: str, *, json_output: bool) -> None:
    """Install a single stdout handler on the root logger. Safe to call more than once."""
    handler = logging.StreamHandler(sys.stdout)
    if json_output:
        handler.setFormatter(JsonFormatter())
    else:
        handler.addFilter(RequestIdFilter())
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-8s [%(request_id)s] %(name)s: %(message)s")
        )

    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)

    for name in _UVICORN_LOGGERS:
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True
    # RequestContextMiddleware writes access logs with request IDs and timings instead.
    logging.getLogger("uvicorn.access").disabled = True
