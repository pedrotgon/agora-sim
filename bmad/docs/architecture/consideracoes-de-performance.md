# Consideracoes de Performance
- Geracao de manual <= 5 min: Whisper executa com GPU se disponivel; fallback CPU com chunking.
- FastAPI configurado com uvicorn --workers 2 --loop uvloop para throughput local.
- Cache de transcricoes em disco (.cache/whisper) para reutilizacao.
- Monitorar tamanho de data/uploads; script de rotacao limpa artefatos antigos.