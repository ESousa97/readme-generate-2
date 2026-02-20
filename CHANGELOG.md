# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [1.5.1] - 2026-02-19

### Changed

- Repository status standardized as archived for study/reference purposes.
- Dependabot configured to stop opening new pull requests.
- Governance documents updated to explicitly state no guarantee of response, review, or fixes.
- Issue and PR templates updated with visible archive notice.
- Issue configuration kept with blank issues disabled and archive notice contact link.

## [1.5.0] - 2026-02-19

### Added

- Repository governance baseline: `.editorconfig`, `.gitignore`, `.gitattributes`, `.env.example`
- Python quality toolchain: `pyproject.toml`, `requirements-dev.txt`
- Unit tests for ZIP extraction utility in `tests/unit/test_utils.py`
- GitHub governance and automation:
  - issue templates
  - PR template
  - CODEOWNERS
  - Dependabot
  - CI and security audit workflows
- Documentation set:
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `SECURITY.md`
  - `docs/architecture.md`, `docs/api.md`, `docs/setup.md`, `docs/deployment.md`

### Changed

- Hardened API defaults:
  - CORS now reads allowed origins from environment
  - Added security HTTP headers middleware
  - Standardized API error response format
- Centralized backend configuration values in `gerador_readme_ia_web/config.py`
- Removed inline styles from `index.html` and added semantic CSS classes/tokens
- Removed frontend debug console logging from tooltip and bootstrap modules
- Rewrote `README.md` to reflect production-grade setup and current architecture

### Fixed

- Security baseline gaps related to permissive CORS and missing response hardening
- Missing local quality validation path (lint/test/audit)

### Security

- Added strict security audit step in CI
- Added private vulnerability disclosure policy in `SECURITY.md`
