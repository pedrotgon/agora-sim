# Requirements

## Functional Requirements

- **FR001**: O sistema deve permitir ao usuário submeter um arquivo de mídia (vídeo, áudio) ou texto para processamento.
- **FR002**: O sistema deve transcrever o conteúdo de mídia usando o Whisper.
- **FR003**: O sistema deve ser capaz de gerar um novo manual (`.docx`) a partir de uma transcrição, usando um modelo de IA para estruturar o conteúdo e um template pré-definido.
- **FR004**: O sistema deve ser capaz de atualizar um manual existente com base em novas instruções ou conteúdo.
- **FR005**: O sistema deve persistir o histórico de interações e documentos em um banco de dados PostgreSQL.
- **FR006**: O sistema deve fornecer uma interface de usuário web (em inglês) para o usuário interagir com o fluxo de documentação.

## Non-Functional Requirements

- **NFR001 (Segurança)**: Todos os dados devem ser processados e armazenados em ambiente **local**. Nenhuma informação sensível deve sair da máquina do usuário, exceto as chamadas para a API de IA permitida.
- **NFR002 (Performance)**: O tempo de geração de um manual (fonte de 10 min) deve ser inferior a 5 minutos, rodando **localmente**.
- **NFR003 (Portabilidade)**: A arquitetura do MVP deve ser projetada para **facilitar a migração futura** para o Google Cloud, mas a implementação do MVP será 100% local.

---
