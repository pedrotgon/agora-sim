# Aido - Detalhamento dos Épicos

Este documento detalha as histórias de usuário para cada um dos épicos definidos no PRD do projeto Aido.

---

## Épico 1: Fundação da Arquitetura de Agentes (ADK) - (Versão Revisada)

**Objetivo**: Implementar a estrutura base do orquestrador e os 3 agentes (`whisper`, `create`, `update`) usando o framework Google ADK para executar o fluxo principal de ponta a ponta localmente.

#### **Histórias de Usuário (Revisadas e Alinhadas com ADK)**

*   **História 1.1**: Como desenvolvedor, quero configurar a estrutura de pastas do projeto seguindo o padrão do Google ADK, com um diretório `agents` contendo subdiretórios para o `aido_orchestrator`, `whisper_agent`, `create_agent` e `update_agent`, para garantir um código organizado e compatível com o framework.

*   **História 1.2**: Como desenvolvedor, quero implementar o `aido_orchestrator` como um **`WorkflowAgent`** no ADK, capaz de gerenciar o estado da conversa e orquestrar a execução dos outros agentes como ferramentas.

*   **História 1.3**: Como desenvolvedor, quero implementar o `whisper_agent` como um **`SequentialAgent`** no ADK. Ele deve:
    1.  Receber o caminho de um arquivo de mídia.
    2.  Utilizar a biblioteca `openai-whisper` para realizar a transcrição localmente.
    3.  Retornar o texto transcrito como sua saída final.

*   **História 1.4**: Como desenvolvedor, quero implementar o `create_agent` como um **`LoopAgent`** no ADK. Ele deve:
    1.  Receber um texto (transcrição) e/ou instruções.
    2.  Interagir com um LLM para gerar um dicionário Python (`context`) contendo os dados estruturados.
    3.  Usar a biblioteca `docxtpl` para preencher o template `Padronizacao_Manuais.docx` com o `context`.
    4.  Encerrar o loop e retornar o caminho do arquivo `.docx` gerado.

*   **História 1.5**: Como desenvolvedor, quero implementar o `update_agent` como um **`LoopAgent`** no ADK, que funcione de forma semelhante ao `create_agent`, mas que também receba o caminho de um `.docx` existente como entrada para o contexto de atualização.

*   **História 1.6**: Como desenvolvedor, quero registrar os agentes (`whisper_agent`, `create_agent`, `update_agent`) como **ferramentas (`tools`)** disponíveis para o `aido_orchestrator` dentro do ambiente ADK, permitindo que ele os invoque dinamicamente.

*   **História 1.7 (Teste de Integração)**: Como usuário, quero executar um fluxo de ponta a ponta via API que invoque o `aido_orchestrator` para transcrever um vídeo (`whisper_agent`) e gerar um novo manual (`create_agent`), para validar a Jornada 1A.

*   **História 1.8 (Teste de Integração)**: Como usuário, quero executar um fluxo de ponta a ponta via API que invoque o `aido_orchestrator` para atualizar um `.docx` existente com novas instruções em texto (`update_agent`), para validar a Jornada 2.

---

## Épico 2: Implementação da Memória e Persistência

**Objetivo**: Integrar o banco de dados PostgreSQL para que o Aido possa armazenar e recuperar o histórico de conversas e manuais.

### Histórias de Usuário

*   **História 2.1**: Como desenvolvedor, quero projetar e criar o schema do banco de dados PostgreSQL com tabelas para armazenar o histórico de chats e metadados de documentos, para estruturar a persistência dos dados.
*   **História 2.2**: Como desenvolvedor, quero criar uma ferramenta de banco de dados (`database_tool`) que o orquestrador possa usar para se conectar e realizar operações de leitura/escrita no PostgreSQL, para abstrair a lógica de acesso aos dados.
*   **História 2.3**: Como usuário, quero que minhas conversas com o Aido sejam salvas automaticamente, para que eu possa fechar e reabrir a aplicação sem perder o contexto.
*   **História 2.4**: Como usuário, quero que o Aido possa recuperar um manual gerado anteriormente a partir do histórico, para facilitar a continuidade do trabalho.

---

## Épico 3: Interface de Usuário Conversacional (UI)

**Objetivo**: Desenvolver a interface de chat (em inglês) baseada no protótipo, permitindo a interação com os agentes.

### Histórias de Usuário

*   **História 3.1**: Como desenvolvedor, quero criar a estrutura de uma aplicação web com o layout de 3 painéis (Processos, Chat, Arquivos) para servir como a base da UI.
*   **História 3.2**: Como usuário, quero ter uma área de chat onde posso digitar minhas instruções e ver tanto as minhas mensagens quanto as respostas do Aido, para poder interagir com o sistema.
*   **História 3.3**: Como desenvolvedor, quero conectar a interface do chat ao backend do `aido_orchestrator`, para permitir a comunicação em tempo real entre o usuário e os agentes.
*   **História 3.4**: Como usuário, quero poder fazer o upload de arquivos (vídeos, áudios, `.docx`) através da interface, para fornecer os insumos necessários para os agentes.
*   **História 3.5**: Como usuário, quero ver indicadores de status na UI (ex: "Transcrevendo...", "Gerando manual..."), para saber o que o Aido está fazendo em tempo real.
*   **História 3.6**: Como usuário, quero receber e poder baixar os manuais `.docx` gerados através da interface, para ter acesso ao resultado final do processo.