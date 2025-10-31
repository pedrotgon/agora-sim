# User Journeys

## Jornada 1: Criação de Manual com `create_agent` (Loop Agent)

*   **Cenário A (com Mídia)**: O usuário fornece um vídeo/áudio. O orquestrador usa o `whisper_agent` para transcrever e depois passa o texto para o `create_agent`, que itera sobre o conteúdo para gerar o `.docx` final.
*   **Cenário B (só com Instruções)**: O usuário fornece as instruções (via chat ou arquivo). O orquestrador aciona diretamente o `create_agent`, que itera sobre as instruções para gerar o `.docx`.

## Jornada 2: Atualização de Manual com `update_agent` (Loop Agent)

*   **Cenário Único**: O usuário fornece um manual `.docx` existente e um conjunto de novas informações, que podem incluir **instruções (via chat/arquivo), novos vídeos/áudios ou outros documentos**. O orquestrador aciona o `update_agent`, que (se necessário) usa o `whisper_agent` para transcrições, e então consolida todas as fontes para gerar a nova versão do `.docx`.

---
