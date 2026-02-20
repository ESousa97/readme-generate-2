# Setup Guide

## Local setup

```bash
git clone https://github.com/ESousa97/readme-generate-2.git
cd readme-generate-2
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

## Recommended environment variables

- `PYTHON_ENV=development`
- `DEBUG=true`
- `CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000`

## Validate locally

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m pip_audit
```
