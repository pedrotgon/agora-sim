# Padroes Inovadores
### Loop de Sintese de Manuais
- Proposito: consolidar midia, instrucoes e versoes anteriores em um manual .docx unico.
- Componentes: orquestrador ADK, whisper_agent, create_agent/update_agent, PostgreSQL, docxtpl.
- Fluxo: upload -> transcricao -> estruturacao JSON -> renderizacao docxtpl -> validacao -> entrega.
- Checkpoints LoopAgent: 	ranscribing -> structuring -> rendering -> validating com eventos SSE (progress.update).
### Sincronizacao de Artefatos Sensiveis
- Proposito: garantir versionamento local e integridade de midia/manuais.
- Componentes: FileArtifactService custom, data/uploads/, tabela manual_versions.
- Estrategia: cada upload recebe hash SHA256; geracoes de manual incrementam versao vinculada ao hash do template e transcricao.