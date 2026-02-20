# API Reference

## Base URL

- Local: `http://127.0.0.1:8000`

## Authentication

- Header required for Gemini-backed endpoints: `X-API-Key: <your-key>`

## `GET /api/list-models`

Lists available Gemini models for the provided API key.

### Headers

- `X-API-Key` (required)

### Success response

```json
{
  "models": [
    {
      "id": "gemini-1.5-flash-latest",
      "name": "Gemini 1.5 Flash",
      "full_name": "models/gemini-1.5-flash-latest"
    }
  ]
}
```

### Error response format

```json
{
  "error": {
    "code": "HTTP_401",
    "message": "API Key não fornecida no cabeçalho X-API-Key para listar modelos."
  }
}
```

## `POST /api/generate-readme`

Generates README markdown from project ZIP and metadata.

### Content-Type

- `multipart/form-data`

### Form fields

- `project_zip` (required, `.zip`)
- `readme_level` (optional: `simple`, `moderate`, `complete`)
- `repo_link` (optional)
- `project_link` (optional)
- `linkedin_link` (optional)
- `requested_badges` (optional, comma-separated)
- `gemini_model_select` (optional)

### Headers

- `X-API-Key` (required)

### Success response

```json
{
  "filename": "project.zip",
  "readme_content": "# Project..."
}
```
