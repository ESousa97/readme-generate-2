# Deployment

## Target

- Render web service (recommended for this project profile)

## Build command

```bash
pip install -r requirements.txt
```

## Start command

```bash
python -m uvicorn api.index:app --host 0.0.0.0 --port $PORT
```

## Required environment variables

- `PORT`
- `PYTHON_ENV=production`
- `DEBUG=false`
- `CORS_ALLOWED_ORIGINS=<your-production-origins>`

## Pre-deploy checklist

1. `python -m ruff check .`
2. `python -m pytest`
3. `python -m pip_audit`
4. Confirm no secrets in tracked files
