# Padroes de Implementacao (Anti-Conflito)
- Naming: REST plural (/projects/{project_id}/messages), tabelas snake_case plural, componentes React PascalCase.
- Estrutura: backend por dominio, frontend por feature, testes em 	ests/{tipo}.
- Formatos: JSON {status,data,meta}, erros {code,message,hint}, datas ISO-8601 UTC.
- Comunicacao: SSE progress.update/manual.ready; eventos ADK tipados (TRANSCRIPTION_READY).
- Ciclo de vida: estados idle|running|waiting_confirmation|completed|error, retries automaticos (2) apenas em Whisper.
- Localizacao: uploads em data/uploads/{project}, template em data/templates/, configs centralizadas em config/settings.py.
- Consistencia: logging JSON com session_id, respostas de UI em ingles, ADRs numeradas em docs/adr/.