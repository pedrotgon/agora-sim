"""FastAPI application exposing the orchestrator endpoints."""

from __future__ import annotations

from fastapi import FastAPI

from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="AIDO Orchestrator API")
    app.include_router(router)
    return app


app = create_app()

