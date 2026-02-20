# Contributing Guide

## Repository Status

This repository is archived and no longer actively maintained.
It remains public for study and reference purposes only.
There is no guarantee of response, review, or fixes for issues and pull requests.

## Development setup

```bash
git clone https://github.com/ESousa97/readme-generate-2.git
cd readme-generate-2
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

## Code style and conventions

- Python lint/format: `ruff` configured in `pyproject.toml`
- Test runner: `pytest`
- Keep modules coesos e sem duplicação
- Não commitar segredos, tokens ou chaves reais

## Branching model

- Branch naming:
  - `feat/<short-description>`
  - `fix/<short-description>`
  - `refactor/<short-description>`
  - `docs/<short-description>`

## Conventional Commits

Formato:

```text
<type>(<scope>): <description>
```

Tipos permitidos:

- `feat` — nova funcionalidade
- `fix` — correção de bug
- `refactor` — refatoração sem mudança de comportamento
- `docs` — documentação
- `style` — formatação sem mudança de lógica
- `test` — adição ou correção de testes
- `chore` — manutenção e dependências
- `ci` — mudanças em CI/CD
- `perf` — melhorias de performance
- `security` — correções de segurança

## Pull request process

1. Abra PR para `main` com descrição técnica clara.
2. Preencha checklist do template de PR.
3. Garanta que CI esteja verde.
4. Aguarde revisão de código do maintainer.

## Local validation

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m pip_audit
```

## Contribution areas

- Cobertura de testes para endpoints e validações
- Melhorias de usabilidade no frontend modular
- Observabilidade e telemetria do backend
- Otimização da extração/análise de ZIP

## Maintainer

- Portfólio: https://enoquesousa.vercel.app
- GitHub: https://github.com/ESousa97
