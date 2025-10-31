# Regras de Consistencia
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