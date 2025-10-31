# Arquitetura de Dados
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