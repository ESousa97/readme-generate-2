# gerador_readme_ia_web/config.py
import os
import logging
from dotenv import load_dotenv

load_dotenv() # Carrega .env para PYTHON_ENV ou GEMINI_MODEL_NAME, se definidos lá

APP_NAME = os.getenv("APP_NAME", "GeradorREADMEWeb")
APP_AUTHOR = os.getenv("APP_AUTHOR", "SousaInfotec")

logger = logging.getLogger(f"{APP_NAME}.config")

DEFAULT_GEMINI_MODEL_WEB = "gemini-1.5-flash-latest"


def get_gemini_model() -> str:
    """
    Obtém o nome do modelo Gemini das variáveis de ambiente ou usa um padrão.
    """
    model_name = os.getenv("GEMINI_MODEL_NAME", DEFAULT_GEMINI_MODEL_WEB)
    if not model_name:
        logger.warning(f"GEMINI_MODEL_NAME não definido, usando padrão: {DEFAULT_GEMINI_MODEL_WEB}")
        return DEFAULT_GEMINI_MODEL_WEB
    logger.debug(f"Usando modelo Gemini: {model_name}")
    return model_name

if __name__ == '__main__':
    print(f"APP_NAME: {APP_NAME}")
    print(f"APP_AUTHOR: {APP_AUTHOR}")
    # print(f"API Key (config servidor, não usado para requisições): {'Configurada' if get_api_key() else 'NÃO CONFIGURADA'}")
    print(f"Modelo Gemini (padrão/config): {get_gemini_model()}")
