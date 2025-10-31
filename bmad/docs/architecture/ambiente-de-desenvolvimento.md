# Ambiente de Desenvolvimento
### Pre-requisitos
- Windows 11 ou WSL2 com 16 GB RAM.
- Python 3.11.x, Node.js 20.x, PostgreSQL 16.x.
- FFmpeg instalado (necessario para Whisper).
- Make opcional (make ou Invoke-Build) para scripts de conveniencia.
### Comandos de Setup
```powershell
# Preparar banco e agentes
python scripts/bootstrap_db.py
python scripts/ingest_reference_docs.py
npm run dev --prefix frontend # inicia UI
uvicorn packages.orchestrator.main:app --reload
## Registros de Decisoes Arquiteturais (ADRs)
- ADR-0001 - Topologia ADK local compartilhada.
- ADR-0002 - PostgreSQL 16.x com SQLAlchemy/Alembic.
- ADR-0003 - Armazenamento data/uploads/ + template corporativo.
- ADR-0004 - FastAPI/Uvicorn + SSE para comunicacao.
- ADR-0005 - Pipeline docxtpl para geracao .docx.
- ADR-0006 - Seguranca local baseada em conta dedicada e DPAPI.
- ADR-0007 - DatabaseSessionService persistente.
- ADR-0008 - LoopAgent com eventos de progresso.
- ADR-0009 - Logging estruturado + dk web.
- ADR-0010 - Integracao UI via cliente HTTP local.
- ADR-0011 - Estrategia Docker/Cloud Run.
- ADR-0012 - Itens postergados (editor colaborativo, Playwright, OpenTelemetry).
---
_Gerado pela BMAD Decision Architecture Workflow v1.0_
_Data: 2025-10-30_
_Para: Pedro_


