# Estrutura de Projeto
```
aido/
|-- .env.example
|-- docker-compose.yml
|-- pyproject.toml
|-- package.json
|-- docs/
|   |-- PRD.md
|   |-- epics.md
|   |-- architecture.md
|   \-- workflows/
|-- data/
|   |-- templates/Padronizacao_Manuais.docx
|   |-- uploads/
|   \-- temp/
|-- logs/
|   \-- app.log
|-- packages/
|   |-- orchestrator/
|   |   |-- app/api/
|   |   |-- app/services/
|   |   |-- app/workflows/
|   |   |-- models/
|   |   |-- migrations/
|   |   \-- main.py
|   |-- agents/
|   |   |-- whisper_agent/
|   |   |-- create_agent/
|   |   |-- update_agent/
|   |   \-- shared/
|   \-- ui-client/
|-- frontend/
|   |-- src/components/
|   |-- src/features/
|   |-- src/services/apiClient.ts
|   |-- src/types/
|   \-- vite.config.ts
|-- scripts/
|   |-- bootstrap_db.py
|   |-- sync_template.py
|   \-- ingest_reference_docs.py
\-- tests/
    |-- unit/
    |-- integration/
    \-- contract/
```
