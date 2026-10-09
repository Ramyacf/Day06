# ft-bvg-backend
This repo is used for the bharatVoiceGuard-backend.
# BharatVoiceGuard Backend

Python/FastAPI modular monolith for the BharatVoiceGuard POC.

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL / Amazon RDS PostgreSQL
- Alembic
- Amazon S3 for audio/report objects
- AWS KMS + Secrets Manager
- Argon2id for passwords

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
uvicorn app.main:app --reload
```

Do not commit `.env`, credentials, audio files, or generated reports.
