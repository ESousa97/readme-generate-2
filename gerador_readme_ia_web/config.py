# gerador_readme_ia_web/config.py
import logging
import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "GeradorREADMEWeb")
APP_AUTHOR = os.getenv("APP_AUTHOR", "SousaInfotec")
PYTHON_ENV = os.getenv("PYTHON_ENV", "production").lower()
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

logger = logging.getLogger(f"{APP_NAME}.config")

DEFAULT_GEMINI_MODEL_WEB = "gemini-1.5-flash-latest"

RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "5"))
RATE_LIMIT_PERIOD_SECONDS = int(os.getenv("RATE_LIMIT_PERIOD_SECONDS", "60"))
BLOCK_TIME_INITIAL_SECONDS = int(os.getenv("BLOCK_TIME_INITIAL_SECONDS", "300"))
BLOCK_TIME_MULTIPLIER = int(os.getenv("BLOCK_TIME_MULTIPLIER", "2"))
MAX_BLOCK_TIME_SECONDS = int(os.getenv("MAX_BLOCK_TIME_SECONDS", "14400"))


def get_gemini_model() -> str:
    model_name = os.getenv("GEMINI_MODEL_NAME", DEFAULT_GEMINI_MODEL_WEB)
    if not model_name:
        logger.warning(
            "GEMINI_MODEL_NAME não definido. Usando padrão '%s'.", DEFAULT_GEMINI_MODEL_WEB
        )
        return DEFAULT_GEMINI_MODEL_WEB
    logger.debug("Usando modelo Gemini: %s", model_name)
    return model_name


def get_cors_allowed_origins() -> list[str]:
    origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]
