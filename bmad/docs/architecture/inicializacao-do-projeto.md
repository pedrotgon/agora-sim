# Inicializacao do Projeto
A primeira historia de implementacao deve preparar o ambiente Python/Node e instalar as dependencias nucleares.
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install "google-adk[database]>=1.17.0" fastapi uvicorn[standard] python-dotenv structlog docxtpl python-docx whisper-timestamped
pip install alembic psycopg[binary]
npm install --prefix frontend
```

Apos esse bootstrap, execute os scripts scripts/bootstrap_db.py e scripts/sync_template.py para criar o schema inicial e copiar 
efs/Padronizacao_Manuais.docx para data/templates/.