"""Logging utilities for the orchestrator runtime."""

from __future__ import annotations

import logging
from typing import Any

try:
    import structlog
except ModuleNotFoundError:  # pragma: no cover - fallback path
    structlog = None  # type: ignore[assignment]


class _StructlogShim:
    """Fallback shim that emulates a minimal structlog interface."""

    def __init__(self, logger: logging.Logger, context: dict[str, Any] | None = None) -> None:
        self._logger = logger
        self._context = context or {}

    def bind(self, **new_context: Any) -> "_StructlogShim":
        context = {**self._context, **new_context}
        return _StructlogShim(self._logger, context)

    def _log(self, level: int, event: str, **kwargs: Any) -> None:
        payload = {**self._context, **kwargs}
        self._logger.log(level, "%s | %s", event, payload)

    def info(self, event: str, **kwargs: Any) -> None:
        self._log(logging.INFO, event, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        self._log(logging.WARNING, event, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        self._log(logging.ERROR, event, **kwargs)

    def debug(self, event: str, **kwargs: Any) -> None:
        self._log(logging.DEBUG, event, **kwargs)

_CONFIGURED = False


def configure_logging(level: int = logging.INFO, **extras: Any) -> None:
    """
    Configure structlog with JSON output and mandatory fields for tracing.

    The configuration is idempotent to avoid duplicated handlers when the
    module is imported by multiple entrypoints (CLI, tests, FastAPI, etc.).
    Additional keyword arguments can be forwarded to ``basicConfig`` to tailor
    log destinations when necessary.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    logging.basicConfig(
        level=level,
        format="%(message)s",
        **extras,
    )

    if structlog:
        structlog.configure(
            cache_logger_on_first_use=True,
            wrapper_class=structlog.make_filtering_bound_logger(level),
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.JSONRenderer(),
            ],
        )

    _CONFIGURED = True


def get_logger():
    """Return a logger bound to the orchestrator component."""
    configure_logging()
    if structlog:
        return structlog.get_logger("aido.orchestrator")
    return _StructlogShim(logging.getLogger("aido.orchestrator"))
