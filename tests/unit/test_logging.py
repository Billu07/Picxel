import json
import logging
import sys
from collections.abc import Iterator

import pytest

from app.core.logging import JsonFormatter, RequestIdFilter, configure_logging, request_id_var


def _record(message: str = "hello", **extra: object) -> logging.LogRecord:
    record = logging.LogRecord("picxel.test", logging.INFO, __file__, 1, message, None, None)
    record.__dict__.update(extra)
    return record


@pytest.fixture
def restore_logging() -> Iterator[None]:
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    access_logger = logging.getLogger("uvicorn.access")
    access_disabled = access_logger.disabled
    yield
    root.handlers[:] = handlers
    root.setLevel(level)
    access_logger.disabled = access_disabled


def test_json_lines_carry_cloud_logging_fields_and_extras() -> None:
    payload = json.loads(JsonFormatter().format(_record(status=200)))

    assert payload["severity"] == "INFO"
    assert payload["message"] == "hello"
    assert payload["logger"] == "picxel.test"
    assert payload["status"] == 200
    assert "request_id" not in payload


def test_json_lines_include_the_current_request_id() -> None:
    token = request_id_var.set("req-12345678")
    try:
        payload = json.loads(JsonFormatter().format(_record()))
    finally:
        request_id_var.reset(token)

    assert payload["request_id"] == "req-12345678"


def test_json_lines_include_tracebacks() -> None:
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.LogRecord(
            "picxel.test", logging.ERROR, __file__, 1, "failed", None, sys.exc_info()
        )

    payload = json.loads(JsonFormatter().format(record))

    assert "ValueError: boom" in payload["exception"]


def test_text_lines_show_a_placeholder_outside_requests() -> None:
    record = _record()

    assert RequestIdFilter().filter(record)
    assert record.__dict__["request_id"] == "-"


@pytest.mark.usefixtures("restore_logging")
def test_configure_logging_installs_one_handler_and_routes_uvicorn_through_it() -> None:
    configure_logging("DEBUG", json_output=True)

    root = logging.getLogger()
    assert len(root.handlers) == 1
    assert isinstance(root.handlers[0].formatter, JsonFormatter)
    assert root.level == logging.DEBUG
    assert logging.getLogger("uvicorn.error").propagate
    assert logging.getLogger("uvicorn.access").disabled
