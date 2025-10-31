# Decision Architecture
## Resumo Executivo
A arquitetura do aido estabelece um ecossistema local de agentes Google ADK coordenados por um orquestrador FastAPI, garantindo confidencialidade e baixa latencia para gerar manuais empresariais. PostgreSQL 16.x prove persistencia transacional, enquanto o pipeline docxtpl assegura que cada manual .docx siga o template corporativo. A UI React se conecta via REST e SSE, oferecendo feedback continuo aos usuarios internos.
## Inicializacao do Projeto
A primeira historia de implementacao deve preparar o ambiente Python/Node e instalar as dependencias nucleares.
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install "google-adk[database]>=1.17.0" fastapi uvicorn[standard] python-dotenv structlog docxtpl python-docx whisper-timestamped
pip install alembic psycopg[binary]
npm install --prefix frontend
```

Apos esse bootstrap, execute os scripts scripts/bootstrap_db.py e scripts/sync_template.py para criar o schema inicial e copiar 
efs/Padronizacao_Manuais.docx para data/templates/.
## Resumo das Decisoes
| Categoria | Decisao | Versao / Estado | Epicos Impactados | Racional |
| --------- | ------- | ---------------- | ----------------- | -------- |
| Orquestracao | Orquestrador ADK local + agentes whisper, create, update no mesmo processo | n/a | 1,2,3 | Mantem latencia minima e preserva confidencialidade dos dados. |
| Persistencia | PostgreSQL local com SQLAlchemy 2.x + Alembic | PostgreSQL 16.x (validar) | 1,2 | Relacionamentos robustos para sessoes, manuais e historico. |
| Armazenamento de Arquivos | Diretorio data/uploads/ para midia e .docx finais | n/a | 1,3 | Garante dados sensiveis on-premise e facilita versionamento. |
| API Backend | FastAPI + Uvicorn servindo REST e SSE | FastAPI 0.111+, Uvicorn 0.30+ (validar) | 1,3 | Framework assincrono tipado, ideal para ADK e UI React. |
| Geracao de Docx | docxtpl sobre template corporativo | docxtpl 0.16+ (validar) | 1,3 | Permite preencher o template mantendo estilos padronizados. |
| Seguranca Local | Execucao sob conta dedicada + .env protegido via DPAPI | n/a | 1,2 | Protege credenciais e restringe acesso ao conjunto de dados. |
| Sessoes ADK | DatabaseSessionService com PostgreSQL | google-adk 1.17+ (validar) | 1,2 | Persistencia confiavel entre reinicios e retomada de contexto. |
| Tarefas Longas | LoopAgent + workers assincronos com eventos de progresso | n/a | 1,3 | Evita bloqueios da UI e fornece checkpoints recuperaveis. |
| Observabilidade | Logging JSON (structlog), dk web, metricas FastAPI | n/a | 1,2 | Auditoria local clara e base para futura observabilidade em cloud. |
| UI <-> Backend | Cliente HTTP/SSE TypeScript substitui geminiService | n/a | 3 | Todas as inferencias permanecem locais e com contrato estavel. |
| Migracao Futura | Docker multi-stage + compose preparado para Cloud Run | Docker 26+ (validar) | 1,3 | Facilita portar componentes para Google Cloud com esforco minimo. |
| Editor Colaborativo | Adiar CRDT/Y.js para fase pos-MVP | Deferido | Futuro | Evita complexidade desnecessaria na primeira entrega. |
| Testes E2E | Planejar Playwright apos estabilizar API | Planejado | Futuro | Prioriza testes unitarios/integrados inicialmente. |
| Observabilidade Avancada | Postergar OpenTelemetry; hooks prontos para futura integracao | Deferido | Futuro | Foco na simplicidade sem impedir evolucao. |
## Estrutura de Projeto
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

## Mapeamento de Epicos para Arquitetura
| Epico | Objetivo | Componentes Principais |
| ----- | -------- | ---------------------- |
| 1. Fundacao ADK | Orquestrar agentes Whisper/Create/Update localmente | packages/orchestrator, packages/agents/*, LoopAgent |
| 2. Persistencia | Persistir historico e artefatos em PostgreSQL | models/, DatabaseSessionService, data/uploads/, migrations/ |
| 3. UI Conversacional | UI web em ingles com chat, uploads e download | rontend/, ui-client/, rotas FastAPI /api/projects, /api/messages |
## Padroes Inovadores
### Loop de Sintese de Manuais
- Proposito: consolidar midia, instrucoes e versoes anteriores em um manual .docx unico.
- Componentes: orquestrador ADK, whisper_agent, create_agent/update_agent, PostgreSQL, docxtpl.
- Fluxo: upload -> transcricao -> estruturacao JSON -> renderizacao docxtpl -> validacao -> entrega.
- Checkpoints LoopAgent: 	ranscribing -> structuring -> rendering -> validating com eventos SSE (progress.update).
### Sincronizacao de Artefatos Sensiveis
- Proposito: garantir versionamento local e integridade de midia/manuais.
- Componentes: FileArtifactService custom, data/uploads/, tabela manual_versions.
- Estrategia: cada upload recebe hash SHA256; geracoes de manual incrementam versao vinculada ao hash do template e transcricao.
## Detalhes da Pilha Tecnologica
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
## Padroes de Implementacao (Anti-Conflito)
- Naming: REST plural (/projects/{project_id}/messages), tabelas snake_case plural, componentes React PascalCase.
- Estrutura: backend por dominio, frontend por feature, testes em 	ests/{tipo}.
- Formatos: JSON {status,data,meta}, erros {code,message,hint}, datas ISO-8601 UTC.
- Comunicacao: SSE progress.update/manual.ready; eventos ADK tipados (TRANSCRIPTION_READY).
- Ciclo de vida: estados idle|running|waiting_confirmation|completed|error, retries automaticos (2) apenas em Whisper.
- Localizacao: uploads em data/uploads/{project}, template em data/templates/, configs centralizadas em config/settings.py.
- Consistencia: logging JSON com session_id, respostas de UI em ingles, ADRs numeradas em docs/adr/.
## Regras de Consistencia
### Naming Conventions
- Classes Python PascalCase, funcoes snake_case.
- Pastas de feature frontend no formato kebab-case (manual-editor).
### Organizacao de Codigo
- Camada pp/services/ concentra integracoes externas.
- pp/workflows/ contem definicoes ADK (Sequential/Loop).
- UI usa hooks especificos (useManualWorkflow) dentro de src/features/workflows.
### Tratamento de Erros
- Excecoes ADK convertidas em HTTPException com payload padronizado.
- UI mostra toasts amigaveis; logs registram error_id correlacionavel.
### Estrategia de Logging
- structlog configura sink para arquivo e console.
- Campos obrigatorios: 	imestamp, level, component, session_id, workflow_step.
## Arquitetura de Dados
### Modelo Relacional
| Tabela | Chaves | Proposito |
| ------ | ------ | --------- |
| projects | id (uuid) | Agrupar uploads, sessoes e manuais. |
| uploads | id, project_id, sha256 | Catalogar midia original e metadados. |
| transcripts | id, upload_id, language, status | Persistir resultados do Whisper. |
| manual_versions | id, project_id, version, docx_path | Historico de manuais gerados, com link para template e transcricao. |
| sessions | id, project_id, state_json | SessionService ADK persistente. |
| events | id, session_id, event_json | Timeline de eventos ADK para auditoria. |
### Artefatos
- data/uploads/: midia original, transcricoes e manuais exportados.
- rtifacts/: diretorio interno do ADK para anexos temporarios (limpeza agendada).
## Contratos de API
| Endpoint | Metodo | Request | Response |
| -------- | ------ | ------- | -------- |
| /api/projects | POST | {name} | {status,data:{project}} |
| /api/projects/{id} | GET | - | {status,data:{project,uploads,manuals}} |
| /api/projects/{id}/uploads | POST (multipart) | arquivo + metadados | {status,data:{upload_id}} |
| /api/projects/{id}/messages | POST | {message, context} | {status,data:{message_id}} (dispara workflow) |
| /api/projects/{id}/stream | GET (SSE) | - | eventos progress.update, manual.ready |
| /api/manuals/{manual_id} | GET | - | download .docx |
Erros seguem {status:"error", errors:[{code,message,hint}]}.
## Arquitetura de Seguranca
- Execucao sob usuario Windows dedicado com permissoes NTFS restritivas (data/, logs/).
- .env criptografado via DPAPI; chaves carregadas em memoria apenas durante o runtime.
- Tokens de sessao (X-AIDO-SESSION) com validade de 15 minutos, renovaveis via refresh local.
- Sem trafego externo exceto chamadas autorizadas para modelos Gemini/Whisper quando configurado.
- Auditoria: logs JSON + tabela events retem acoes relevantes para compliance.
## Consideracoes de Performance
- Geracao de manual <= 5 min: Whisper executa com GPU se disponivel; fallback CPU com chunking.
- FastAPI configurado com uvicorn --workers 2 --loop uvloop para throughput local.
- Cache de transcricoes em disco (.cache/whisper) para reutilizacao.
- Monitorar tamanho de data/uploads; script de rotacao limpa artefatos antigos.
## Arquitetura de Deploy
- Ambiente padrao: docker-compose com servicos pp, postgres, rontend e pgadmin opcional.
- Build multi-stage: estagio base Python instala dependencias, estagio Node compila UI, estagio final combina assets.
- Preparacao para Google Cloud Run: container unico com variaveis DATABASE_URL, GEMINI_API_KEY, STORAGE_ROOT.
- Backups automaticos PostgreSQL via pg_dump (script em scripts/backup_db.ps1).
## Ambiente de Desenvolvimento
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


