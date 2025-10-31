"""Session service abstractions used by the orchestrator workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from google.adk.sessions import BaseSessionService, InMemorySessionService


SessionServiceFactory = Callable[[], BaseSessionService]


@dataclass
class SessionServiceManager:
    """
    Holds the session service used by the orchestrator.

    The initial implementation leverages the in-memory service provided by ADK
    so that all tests and local executions run without external dependencies.
    The manager exposes ``swap`` to make it trivial to inject a persistent
    implementation (e.g., DatabaseSessionService) in future epics.
    """

    session_service: BaseSessionService

    @classmethod
    def in_memory(cls) -> "SessionServiceManager":
        return cls(session_service=InMemorySessionService())

    @classmethod
    def from_factory(
        cls,
        factory: Optional[SessionServiceFactory] = None,
    ) -> "SessionServiceManager":
        factory = factory or InMemorySessionService
        return cls(session_service=factory())

    def swap(self, new_service: BaseSessionService) -> None:
        """Replace the managed session service at runtime."""
        self.session_service = new_service

