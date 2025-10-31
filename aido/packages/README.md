# Estrutura de pacotes

Este diretório segue a topologia definida para o Google ADK, separando orquestrador e agentes:

- `orchestrator/`: mantém os fluxos principais e integrações de runtime.
- `agents/`: concentra os agentes especializados consumidos pelo orquestrador.
  - `whisper_agent/`
  - `create_agent/`
  - `update_agent/`
  - `shared/`

A estrutura preserva o isolamento do orquestrador e permite referenciar os agentes como ferramentas reutilizáveis dentro do runtime ADK.