# Arquitetura de Seguranca
- Execucao sob usuario Windows dedicado com permissoes NTFS restritivas (data/, logs/).
- .env criptografado via DPAPI; chaves carregadas em memoria apenas durante o runtime.
- Tokens de sessao (X-AIDO-SESSION) com validade de 15 minutos, renovaveis via refresh local.
- Sem trafego externo exceto chamadas autorizadas para modelos Gemini/Whisper quando configurado.
- Auditoria: logs JSON + tabela events retem acoes relevantes para compliance.