# Mapeamento de Epicos para Arquitetura
| Epico | Objetivo | Componentes Principais |
| ----- | -------- | ---------------------- |
| 1. Fundacao ADK | Orquestrar agentes Whisper/Create/Update localmente | packages/orchestrator, packages/agents/*, LoopAgent |
| 2. Persistencia | Persistir historico e artefatos em PostgreSQL | models/, DatabaseSessionService, data/uploads/, migrations/ |
| 3. UI Conversacional | UI web em ingles com chat, uploads e download | rontend/, ui-client/, rotas FastAPI /api/projects, /api/messages |