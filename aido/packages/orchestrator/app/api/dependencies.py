"""Dependency wiring for FastAPI routes."""

from __future__ import annotations

from functools import lru_cache

from ..services.logging import configure_logging
from ..workflows.aido_orchestrator import WorkflowAgent, build_default_workflow


@lru_cache
def _workflow_runtime() -> WorkflowAgent:
    configure_logging()
    return build_default_workflow()


def get_workflow_agent() -> WorkflowAgent:
    """FastAPI dependency that returns the singleton workflow agent."""
    return _workflow_runtime()
