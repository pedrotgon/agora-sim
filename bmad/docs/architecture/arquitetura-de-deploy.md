# Arquitetura de Deploy
- Ambiente padrao: docker-compose com servicos pp, postgres, rontend e pgadmin opcional.
- Build multi-stage: estagio base Python instala dependencias, estagio Node compila UI, estagio final combina assets.
- Preparacao para Google Cloud Run: container unico com variaveis DATABASE_URL, GEMINI_API_KEY, STORAGE_ROOT.
- Backups automaticos PostgreSQL via pg_dump (script em scripts/backup_db.ps1).