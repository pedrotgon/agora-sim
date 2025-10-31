# Detalhes da Pilha Tecnologica
### Tecnologias Centrais
- Python 3.11 e google-adk 1.17.x (validar versoes na instalacao).
- FastAPI 0.111+, Uvicorn 0.30+, pydantic v2 para validacao.
- PostgreSQL 16.x com SQLAlchemy 2.x, Alembic para migrations.
- Whisper local (whisper-timestamped) com FFmpeg instalado.
- docxtpl 0.16+ e python-docx para geracao de manuais.
- React 18 + Vite + TypeScript 5 na UI, Tailwind CSS opcional.
- structlog para logging JSON, pytest/httpx para testes.
### Integracoes Internas
1. UI -> FastAPI: REST JSON e SSE via EventSource para progresso.
2. FastAPI -> Orquestrador: chamadas Python nativas para runners ADK.
3. Orquestrador -> Agentes: Sequential/Loop Agents definidos em pp/workflows/.
4. Agentes -> PostgreSQL: DatabaseSessionService + repositorios SQLAlchemy.
5. Agente create -> docxtpl: renderizacao com dados estruturados.
6. Agente whisper -> Whisper local: transcricao off-line com fallback CPU.