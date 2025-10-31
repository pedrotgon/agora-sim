"""HTTP endpoints exposing the orchestrator workflow."""

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from ..services.logging import get_logger
from ..workflows.aido_orchestrator import (
    MessageNotFoundError,
    MessageProjectMismatchError,
    WorkflowAgent,
    WorkflowEvent,
)
from .dependencies import get_workflow_agent

router = APIRouter(prefix="/api/projects", tags=["orchestrator"])
logger = get_logger().bind(component="api")


class MessageRequest(BaseModel):
    message: str = Field(..., description="Texto informado pelo usuário final.")
    context: Dict[str, str] | None = Field(
        default=None,
        description="Metadados opcionais (não processados neste MVP).",
    )


class MessageResponse(BaseModel):
    status: str = "ok"
    data: Dict[str, str]


@router.post(
    "/{project_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def enqueue_message(
    project_id: str,
    request: MessageRequest,
    orchestrator: WorkflowAgent = Depends(get_workflow_agent),
) -> JSONResponse:
    message_id = await orchestrator.submit_message(
        project_id=project_id,
        message=request.message,
    )
    logger.info(
        "message_enqueued",
        project_id=project_id,
        message_id=message_id,
    )
    body = MessageResponse(data={"message_id": message_id})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=body.model_dump())


@router.get(
    "/{project_id}/stream",
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
)
async def stream_updates(
    project_id: str,
    message_id: str,
    orchestrator: WorkflowAgent = Depends(get_workflow_agent),
) -> StreamingResponse:
    async def event_iterator() -> AsyncGenerator[str, None]:
        try:
            async for workflow_event in orchestrator.stream_for_message(
                project_id=project_id,
                message_id=message_id,
            ):
                yield _format_sse(workflow_event)
        except MessageNotFoundError as exc:
            logger.warning(
                "message_not_found",
                project_id=project_id,
                message_id=message_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        except MessageProjectMismatchError as exc:
            logger.warning(
                "message_project_mismatch",
                project_id=project_id,
                message_id=message_id,
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc

    return StreamingResponse(
        event_iterator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


def _format_sse(event: WorkflowEvent) -> str:
    """
    Convert the normalized workflow event into the SSE wire format.
    """
    payload = json.dumps(event.payload, ensure_ascii=False)
    return f"event: {event.event_type}\ndata: {payload}\n\n"

