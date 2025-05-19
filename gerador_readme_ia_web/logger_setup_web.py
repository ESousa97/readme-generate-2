# gerador_readme_ia_web/logger_setup_web.py
import logging
import sys
import os
from logging.handlers import RotatingFileHandler # Pode ser útil para desenvolvimento local
# from appdirs import user_log_dir # Menos relevante para apps web serverless

# Importa APP_AUTHOR das configurações web para consistência
# from .config import APP_AUTHOR as DEFAULT_APP_AUTHOR # Removido para evitar importação circular se config usar logger

LOG_FILE_NAME_DEFAULT = "app_web.log"

def setup_logging(logger_name: str,
                  debug: bool = False,
                  log_file_name: str = LOG_FILE_NAME_DEFAULT,
                  app_author: str = "DefaultAppAuthorWeb", # Padrão se não vier de config
                  is_web_app: bool = False): # Flag para diferenciar config de web app
    """Configura o logging para a aplicação web."""
    logger = logging.getLogger(logger_name)
    
    # Evitar adicionar múltiplos handlers se já configurado
    if logger.hasHandlers() and not getattr(logger, '_configured_for_web', False):
        logger.handlers.clear() # Limpa handlers antigos se reconfigurando

    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')

    # Console Handler (para stdout/stderr, que a Vercel captura)
    ch = logging.StreamHandler(sys.stdout) # Ou sys.stderr para logs de erro
    ch.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler (opcional, mais para desenvolvimento local, Vercel não persiste arquivos assim)
    if not is_web_app or os.getenv("PYTHON_ENV") == "development": # Só loga em arquivo localmente
        try:
            # Para desenvolvimento local, pode-se logar em um arquivo.
            # Em um ambiente serverless como Vercel, o logging em arquivo não é persistente.
            # O diretório de logs pode ser o diretório raiz do projeto para simplicidade local.
            log_dir_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs") # Ex: logs/ na raiz
            if not os.path.exists(log_dir_local):
                os.makedirs(log_dir_local, exist_ok=True)
            
            log_file_path = os.path.join(log_dir_local, log_file_name)

            fh = RotatingFileHandler(log_file_path, maxBytes=1*1024*1024, backupCount=3, encoding='utf-8')
            fh.setLevel(logging.DEBUG) # Logar tudo no arquivo localmente
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.info(f"Logging para '{logger_name}' configurado. Saída para console. Log de arquivo local (se dev): {log_file_path}")
        except Exception as e:
            # Usar print para stderr em caso de falha na configuração do logger de arquivo
            print(f"[CRITICAL_LOGGER_ERROR] Erro ao configurar o file handler do log para '{logger_name}': {e}", file=sys.stderr)
            logger.warning(f"Logging de arquivo desabilitado para '{logger_name}' devido a erro: {e}")
    else:
        logger.info(f"Logging para '{logger_name}' configurado. Saída para console (ambiente web/Vercel).")

    setattr(logger, '_configured_for_web', True) # Marca que foi configurado
    return logger
