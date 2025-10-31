"""AIDO orchestrator workflow built on top of Google ADK."""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, Optional

try:
    import structlog
except ModuleNotFoundError:  # pragma: no cover - fallback path
    structlog = None
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.runners import Runner
from google.adk.sessions import BaseSessionService
from google.genai import types

from ..services.logging import get_logger
from ..services.session import SessionServiceManager


@dataclass(slots=True)
class WorkflowEvent:
    """Normalized event emitted to the SSE layer."""

    event_type: str
    payload: Dict[str, Any]


class MessageNotFoundError(RuntimeError):
    """Raised when a consumer requests a message that was not submitted."""


class MessageProjectMismatchError(RuntimeError):
    """Raised when the requested message does not belong to the provided project."""


class BootstrapWorkflowAgent(BaseAgent):
    """
    Minimal bootstrap agent that simulates the orchestration flow.

    The real implementation will be replaced in later stories once the
    dedicated agents are in place, but this agent allows the runtime to be
    exercised end-to-end (tests, FastAPI, SSE) without calling remote LLMs.
    """

    name: str = "aido_orchestrator"
    description: str = (
        "Orquestrador inicial do AIDO. Simula as etapas principais do workflow "
        "enquanto os agentes especializados não estão disponíveis."
    )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        user_message = self._extract_user_message(ctx)

        yield self._progress_event(
            ctx=ctx,
            message="Analisando solicitação do usuário...",
            step="analisar_pedido",
        )
        await asyncio.sleep(0)

        yield self._progress_event(
            ctx=ctx,
            message=f"Coordenando agentes para: {user_message or 'solicitação'}",
            step="coordenar_agentes",
        )
        await asyncio.sleep(0)

        manual_path = f"/manuals/{uuid.uuid4().hex}.docx"
        yield self._manual_ready_event(
            ctx=ctx,
            message=f"Manual gerado e disponível em {manual_path}",
            manual_path=manual_path,
        )

    def _extract_user_message(self, ctx: InvocationContext) -> str:
        if not ctx.user_content or not ctx.user_content.parts:
            return ""
        texts = [part.text for part in ctx.user_content.parts if part.text]
        return "\n".join(texts)

    def _progress_event(self, *, ctx: InvocationContext, message: str, step: str) -> Event:
        content = types.Content(role="assistant", parts=[types.Part.from_text(text=message)])
        actions = EventActions(agent_state={"step": step})
        return Event(
            invocation_id=ctx.invocation_id,
            author=self.name,
            branch=ctx.branch,
            content=content,
            actions=actions,
        )

    def _manual_ready_event(
        self,
        *,
        ctx: InvocationContext,
        message: str,
        manual_path: str,
    ) -> Event:
        content = types.Content(role="assistant", parts=[types.Part.from_text(text=message)])
        actions = EventActions(
            agent_state={"step": "manual_concluido"},
            state_delta={"manual_ready": True, "manual_path": manual_path},
        )
        return Event(
            invocation_id=ctx.invocation_id,
            author=self.name,
            branch=ctx.branch,
            content=content,
            actions=actions,
        )


class WorkflowAgent:
    """
    High level orchestrator that wraps the ADK runner and normalizes events.
    """

    def __init__(
        self,
        *,
        runner: Runner,
        session_manager: SessionServiceManager,
        user_id: str = "aido_backend",
        logger: Optional[Any] = None,
    ) -> None:
        self.runner = runner
        self.session_manager = session_manager
        self.user_id = user_id
        base_logger = logger or get_logger()
        if structlog and hasattr(base_logger, "bind"):
            self._logger = base_logger.bind(
                component="workflow", agent=self.runner.agent.name
            )
        else:
            self._logger = base_logger

        self._pending_messages: dict[str, tuple[str, str]] = {}
        self._pending_lock = asyncio.Lock()

    @property
    def session_service(self) -> BaseSessionService:
        return self.session_manager.session_service

    async def submit_message(self, *, project_id: str, message: str) -> str:
        """
        Register a message for processing and return a correlation identifier.
        """
        message_id = uuid.uuid4().hex
        async with self._pending_lock:
            self._pending_messages[message_id] = (project_id, message)
        self._logger.info(
            "message_submitted",
            session_id=project_id,
            workflow_step="submitted",
            message_id=message_id,
        )
        return message_id

    async def stream_for_message(
        self, *, project_id: str, message_id: str
    ) -> AsyncGenerator[WorkflowEvent, None]:
        """
        Stream workflow events associated with a previously submitted message.
        """
        async with self._pending_lock:
            try:
                stored_project_id, message = self._pending_messages.pop(message_id)
            except KeyError as exc:
                raise MessageNotFoundError(message_id) from exc

        if stored_project_id != project_id:
            raise MessageProjectMismatchError(
                f"Mensagem {message_id} pertence ao projeto {stored_project_id}"
            )

        async for event in self._stream_message(
            project_id=stored_project_id,
            message=message,
            message_id=message_id,
        ):
            yield event

    async def _stream_message(
        self,
        *,
        project_id: str,
        message: str,
        message_id: str,
    ) -> AsyncGenerator[WorkflowEvent, None]:
        session = await self._ensure_session(session_id=project_id)
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)],
        )

        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=session.id,
            new_message=content,
        ):
            workflow_event = self._normalize_event(
                event=event,
                session_id=session.id,
                message_id=message_id,
            )
            self._logger.info(
                "workflow_event",
                event_type=workflow_event.event_type,
                session_id=session.id,
                workflow_step=workflow_event.payload["workflow_step"],
                message_id=message_id,
            )
            yield workflow_event

    async def _ensure_session(self, *, session_id: str):
        session = await self.session_service.get_session(
            app_name=self.runner.app_name,
            user_id=self.user_id,
            session_id=session_id,
        )
        if session is None:
            session = await self.session_service.create_session(
                app_name=self.runner.app_name,
                user_id=self.user_id,
                session_id=session_id,
                state={"project_id": session_id},
            )
            self._logger.info(
                "session_created",
                session_id=session.id,
                workflow_step="session_setup",
            )
        return session

    def _normalize_event(
        self,
        *,
        event: Event,
        session_id: str,
        message_id: str,
    ) -> WorkflowEvent:
        event_type = self._resolve_event_type(event)
        workflow_step = self._resolve_workflow_step(event)
        payload: Dict[str, Any] = {
            "message_id": message_id,
            "session_id": session_id,
            "workflow_step": workflow_step,
            "message": self._extract_text(event),
            "state_delta": event.actions.state_delta or {},
            "timestamp": event.timestamp,
        }
        return WorkflowEvent(event_type=event_type, payload=payload)

    def _resolve_event_type(self, event: Event) -> str:
        state_delta = event.actions.state_delta or {}
        if state_delta.get("manual_ready"):
            return "manual.ready"
        return "progress.update"

    def _resolve_workflow_step(self, event: Event) -> str:
        agent_state = event.actions.agent_state or {}
        return str(agent_state.get("step") or event.author or "desconhecido")

    def _extract_text(self, event: Event) -> str:
        if not event.content or not event.content.parts:
            return ""
        parts = [part.text for part in event.content.parts if part.text]
        return "\n".join(parts)


def build_default_workflow() -> WorkflowAgent:
    """
    Factory that wires the bootstrap agent with the ADK runner and session service.
    """
    session_manager = SessionServiceManager.in_memory()
    agent: BaseAgent = BootstrapWorkflowAgent()
    runner = Runner(
        app_name=agent.name,
        agent=agent,
        session_service=session_manager.session_service,
    )
    logger = get_logger()
    return WorkflowAgent(runner=runner, session_manager=session_manager, logger=logger)
