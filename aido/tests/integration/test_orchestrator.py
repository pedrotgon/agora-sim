"""Integration coverage for the orchestrator workflow and FastAPI adapters."""

from __future__ import annotations

import json

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from aido.packages.orchestrator.app.api.app import create_app
from aido.packages.orchestrator.app.api.dependencies import get_workflow_agent
from aido.packages.orchestrator.app.workflows.aido_orchestrator import (
    WorkflowAgent,
    build_default_workflow,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_workflow_stream_emits_progress_and_manual_ready() -> None:
    orchestrator = build_default_workflow()
    message_id = await orchestrator.submit_message(
        project_id="proj-1",
        message="Preparar manual inicial",
    )

    events = [
        event
        async for event in orchestrator.stream_for_message(
            project_id="proj-1",
            message_id=message_id,
        )
    ]

    assert events, "O workflow deve emitir ao menos um evento."
    assert events[0].event_type == "progress.update"

    final_event = events[-1]
    assert final_event.event_type == "manual.ready"
    assert final_event.payload["state_delta"]["manual_ready"] is True
    assert final_event.payload["workflow_step"] == "manual_concluido"


@pytest.mark.anyio
async def test_fastapi_stream_endpoint_returns_sse() -> None:
    orchestrator: WorkflowAgent = build_default_workflow()
    app: FastAPI = create_app()
    app.dependency_overrides[get_workflow_agent] = lambda: orchestrator

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        enqueue = await client.post(
            "/api/projects/proj-99/messages",
            json={"message": "Gerar manual de boas práticas"},
        )
        assert enqueue.status_code == 202
        message_id = enqueue.json()["data"]["message_id"]

        async with client.stream(
            "GET",
            "/api/projects/proj-99/stream",
            params={"message_id": message_id},
        ) as stream:
            assert stream.status_code == 200
            body = ""
            async for chunk in stream.aiter_text():
                body += chunk

    events = [block for block in body.strip().split("\n\n") if block]
    assert events, "O SSE deve retornar ao menos um bloco de evento."

    assert events[0].startswith("event: progress.update")
    assert events[-1].startswith("event: manual.ready")

    data_line = next(line for line in events[-1].splitlines() if line.startswith("data: "))
    payload = json.loads(data_line.removeprefix("data: "))
    assert payload["state_delta"]["manual_ready"] is True
    assert payload["workflow_step"] == "manual_concluido"

    # Limpeza da sobreposição das dependências para evitar vazamento entre testes.
    app.dependency_overrides.clear()
