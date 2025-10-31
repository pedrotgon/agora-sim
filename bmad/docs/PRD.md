# aido Product Requirements Document (PRD)

**Author:** Pedro
**Date:** 2025-10-30
**Project Level:** {{project_level}}
**Target Scale:** {{target_scale}}

---

## Goals and Background Context

### Goals

- **Entregar um MVP funcional** que valide a arquitetura de agentes (ADK) para automação de documentos até 29/12.
- **Reduzir o tempo de criação de manuais** em pelo menos 75% para os usuários-alvo.
- **Garantir a segurança e a confidencialidade** dos dados da empresa ao operar como uma solução interna.
- **Provar o valor da inovação interna**, fornecendo um caso de uso de sucesso para a diretoria.

### Background Context

O Aido surge para resolver a ineficiência e a perda de conhecimento no processo de documentação da empresa. A abordagem atual, manual e inconsistente, representa um custo operacional e um risco estratégico. O projeto é uma iniciativa de inovação interna, com apoio da diretoria, que visa criar uma ferramenta segura e escalável para automatizar a criação de manuais padronizados a partir de diversas fontes, como vídeos e textos.

---

## Requirements

### Functional Requirements

- **FR001**: O sistema deve permitir ao usuário submeter um arquivo de mídia (vídeo, áudio) ou texto para processamento.
- **FR002**: O sistema deve transcrever o conteúdo de mídia usando o Whisper.
- **FR003**: O sistema deve ser capaz de gerar um novo manual (`.docx`) a partir de uma transcrição, usando um modelo de IA para estruturar o conteúdo e um template pré-definido.
- **FR004**: O sistema deve ser capaz de atualizar um manual existente com base em novas instruções ou conteúdo.
- **FR005**: O sistema deve persistir o histórico de interações e documentos em um banco de dados PostgreSQL.
- **FR006**: O sistema deve fornecer uma interface de usuário web (em inglês) para o usuário interagir com o fluxo de documentação.

### Non-Functional Requirements

- **NFR001 (Segurança)**: Todos os dados devem ser processados e armazenados em ambiente **local**. Nenhuma informação sensível deve sair da máquina do usuário, exceto as chamadas para a API de IA permitida.
- **NFR002 (Performance)**: O tempo de geração de um manual (fonte de 10 min) deve ser inferior a 5 minutos, rodando **localmente**.
- **NFR003 (Portabilidade)**: A arquitetura do MVP deve ser projetada para **facilitar a migração futura** para o Google Cloud, mas a implementação do MVP será 100% local.

---

## User Journeys

### Jornada 1: Criação de Manual com `create_agent` (Loop Agent)

*   **Cenário A (com Mídia)**: O usuário fornece um vídeo/áudio. O orquestrador usa o `whisper_agent` para transcrever e depois passa o texto para o `create_agent`, que itera sobre o conteúdo para gerar o `.docx` final.
*   **Cenário B (só com Instruções)**: O usuário fornece as instruções (via chat ou arquivo). O orquestrador aciona diretamente o `create_agent`, que itera sobre as instruções para gerar o `.docx`.

### Jornada 2: Atualização de Manual com `update_agent` (Loop Agent)

*   **Cenário Único**: O usuário fornece um manual `.docx` existente e um conjunto de novas informações, que podem incluir **instruções (via chat/arquivo), novos vídeos/áudios ou outros documentos**. O orquestrador aciona o `update_agent`, que (se necessário) usa o `whisper_agent` para transcrições, e então consolida todas as fontes para gerar a nova versão do `.docx`.

---

## UX Design Principles

- **Conversacional**: A interação principal é através de linguagem natural, como em um chat.
- **Clareza de Status**: O usuário deve ser sempre informado sobre o que está acontecendo (e.g., 'Processando...', 'Manual pronto').
- **Foco na Tarefa**: A interface deve ser minimalista, focada na tarefa de criar ou atualizar um manual.

---

## User Interface Design Goals

- **Layout de 3 Painéis**: Manter a estrutura do protótipo, com painéis para **Processos**, Chat e Arquivos.
- **Componentes Interativos**: Incluir elementos como barras de progresso e pré-visualização de Markdown no chat.

---

## Epic List

- **Épico 1: Fundação da Arquitetura de Agentes (ADK)**
  - **Objetivo**: Implementar a estrutura base do orquestrador e os 3 agentes (`whisper`, `create`, `update`) para executar o fluxo principal de ponta a ponta localmente.
  - *Estimativa de Histórias: 8-10*
- **Épico 2: Implementação da Memória e Persistência**
  - **Objetivo**: Integrar o banco de dados PostgreSQL para que o Aido possa armazenar e recuperar o histórico de conversas e manuais.
  - *Estimativa de Histórias: 3-5*
- **Épico 3: Interface de Usuário Conversacional (UI)**
  - **Objetivo**: Desenvolver a interface de chat (em inglês) baseada no protótipo, permitindo a interação com os agentes.
  - *Estimativa de Histórias: 5-7*

> **Note:** Detailed epic breakdown with full story specifications is available in [epics.md](./epics.md)

---

## Out of Scope

- **Suporte a Múltiplos Idiomas na UI**: A interface será exclusivamente em inglês.
- **Deploy no Google Cloud**: O MVP será 100% local. A migração para a nuvem é uma fase futura.
- **Dashboards de Análise**: Qualquer funcionalidade de análise preditiva ou BI.
- **UI Avançada**: O uso de componentes de design avançados (como Shadcn).
- **Outros Formatos de Saída**: O foco é exclusivamente em `.docx`.
