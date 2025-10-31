# Resumo das Decisoes
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