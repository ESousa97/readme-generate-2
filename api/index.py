# api/index.py
import os
import re  # Importar regex para parsing de mensagens de erro
import sys
import tempfile
import time
from collections import defaultdict
from typing import Annotated, Optional

import uvicorn
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(current_file_dir)
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

import google.generativeai as genai_core

# Importar exceções específicas da google-api-core se necessário para uma captura mais fina no futuro
# from google.api_core.exceptions import ResourceExhausted, InvalidArgument, PermissionDenied
from gerador_readme_ia_web.config import (
    APP_AUTHOR,
    APP_NAME,
    BLOCK_TIME_INITIAL_SECONDS,
    BLOCK_TIME_MULTIPLIER,
    DEBUG,
    MAX_BLOCK_TIME_SECONDS,
    RATE_LIMIT_PERIOD_SECONDS,
    RATE_LIMIT_REQUESTS,
    get_cors_allowed_origins,
    get_gemini_model,
)
from gerador_readme_ia_web.constants_web import (
    PROMPT_README_COMPLETE,
    PROMPT_README_MODERATE,
    PROMPT_README_SIMPLE,
    USER_LINKS_INSTRUCTIONS_TEMPLATE,
)
from gerador_readme_ia_web.gemini_client_web import GeminiClient
from gerador_readme_ia_web.logger_setup_web import setup_logging
from gerador_readme_ia_web.utils import extract_project_data_from_zip

logger = setup_logging(f"{APP_NAME}.api", app_author=APP_AUTHOR, debug=DEBUG, is_web_app=True)
logger.info(f"Sistema Operacional detectado (os.name): {os.name}")

app = FastAPI(
    title="Gerador de README.md API",
    description="API para gerar README.md com níveis de detalhe, informações opcionais, seleção de badges e modelos Gemini.",
    version="1.4.2",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

public_dir = os.path.join(project_root_dir, "public")
if not os.path.exists(public_dir):
    os.makedirs(public_dir, exist_ok=True)
    logger.info(f"Diretório público '{public_dir}' criado.")
app.mount("/public", StaticFiles(directory=public_dir), name="public")

RATE_LIMIT_STORE = defaultdict(
    lambda: {"requests": 0, "first_request_time": 0.0, "block_until": 0.0, "offenses": 0}
)
CLEANUP_INTERVAL_SECONDS = 3600
last_cleanup_time = time.time()


def error_payload(code: str, message: str, details: Optional[object] = None) -> dict:
    payload = {"error": {"code": code, "message": message}}
    if DEBUG and details is not None:
        payload["error"]["details"] = details
    return payload


@app.middleware("http")
async def secure_response_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com data:; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net; connect-src 'self';"
    )
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(code=f"HTTP_{exc.status_code}", message=str(exc.detail)),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_payload(
            code="REQUEST_VALIDATION_ERROR",
            message="Dados da requisição inválidos.",
            details=exc.errors(),
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.critical("Erro não tratado na aplicação", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_payload(
            code="INTERNAL_SERVER_ERROR",
            message="Erro interno inesperado no servidor.",
            details=str(exc),
        ),
    )


async def rate_limit_checker(request: Request):
    global last_cleanup_time
    client_ip = request.client.host
    current_time = time.time()

    if current_time - last_cleanup_time > CLEANUP_INTERVAL_SECONDS:
        logger.info("Executando limpeza de entradas antigas do rate limit.")
        ips_to_remove = [
            ip
            for ip, data in RATE_LIMIT_STORE.items()
            if data["block_until"] < current_time - MAX_BLOCK_TIME_SECONDS * 2
        ]
        for ip in ips_to_remove:
            del RATE_LIMIT_STORE[ip]
        last_cleanup_time = current_time
        logger.info(f"Limpeza concluída. {len(ips_to_remove)} IPs removidos.")

    ip_data = RATE_LIMIT_STORE[client_ip]

    if ip_data["block_until"] > current_time:
        block_remaining = int(ip_data["block_until"] - current_time)
        logger.warning(
            f"IP {client_ip} bloqueado. Tempo restante: {block_remaining}s. Ofensas: {ip_data['offenses']}"
        )
        raise HTTPException(
            status_code=429,
            detail=f"Você fez muitas requisições. Tente novamente em {block_remaining} segundos. Bloqueio progressivo ativo.",
        )

    if current_time - ip_data["first_request_time"] > RATE_LIMIT_PERIOD_SECONDS:
        ip_data["requests"] = 0
        ip_data["first_request_time"] = current_time

    ip_data["requests"] += 1

    if ip_data["requests"] > RATE_LIMIT_REQUESTS:
        ip_data["offenses"] += 1
        block_duration = BLOCK_TIME_INITIAL_SECONDS * (
            BLOCK_TIME_MULTIPLIER ** (ip_data["offenses"] - 1)
        )
        block_duration = min(block_duration, MAX_BLOCK_TIME_SECONDS)
        ip_data["block_until"] = current_time + block_duration
        ip_data["requests"] = 0
        ip_data["first_request_time"] = current_time
        logger.warning(
            f"IP {client_ip} excedeu o limite de requisições ({RATE_LIMIT_REQUESTS}/{RATE_LIMIT_PERIOD_SECONDS}s). Bloqueando por {block_duration}s. Total de ofensas: {ip_data['offenses']}"
        )
        raise HTTPException(
            status_code=429,
            detail=f"Você excedeu o limite de requisições. Bloqueado por {int(block_duration)} segundos. O tempo de bloqueio aumenta a cada infração.",
        )
    logger.debug(f"IP {client_ip} - Requisições no período: {ip_data['requests']}")


@app.get("/api/list-models")
async def list_models_endpoint(
    user_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
):
    if not user_api_key:
        logger.warning("X-API-Key não fornecida para /api/list-models.")
        raise HTTPException(
            status_code=401,
            detail="API Key não fornecida no cabeçalho X-API-Key para listar modelos.",
        )
    try:
        genai_core.configure(api_key=user_api_key)
        models_data = []
        for model in genai_core.list_models():
            if "generateContent" in model.supported_generation_methods:
                model_name_simple = model.name.replace("models/", "")
                models_data.append(
                    {"id": model_name_simple, "name": model.display_name, "full_name": model.name}
                )

        relevant_models_output = []
        default_model_from_env = get_gemini_model().replace("models/", "")
        default_model_info = next(
            (m for m in models_data if m["id"] == default_model_from_env), None
        )
        if default_model_info:
            relevant_models_output.append(default_model_info)

        for model_info in models_data:
            if "gemini" in model_info["id"].lower() and model_info["id"] != default_model_from_env:
                relevant_models_output.append(model_info)

        if not default_model_info and default_model_from_env:
            relevant_models_output.insert(
                0,
                {
                    "id": default_model_from_env,
                    "name": f"{default_model_from_env} (Padrão do Sistema)",
                    "full_name": f"models/{default_model_from_env}",
                },
            )

        logger.info(
            f"Modelos Gemini listados para seleção (usando chave do usuário): {[m['id'] for m in relevant_models_output]}"
        )
        return JSONResponse(content={"models": relevant_models_output})
    except Exception as e:
        logger.error(f"Erro ao listar modelos Gemini com chave do usuário: {e}", exc_info=True)
        detail_msg = f"Erro ao listar modelos: {str(e)}. Verifique se a API Key fornecida tem permissão para listar modelos."
        # Erros comuns da API Gemini para chaves inválidas ou sem permissão
        if (
            "API key not valid" in str(e).lower()
            or "API_KEY_INVALID" in str(e).upper()
            or ("PermissionDenied" in str(type(e).__name__) and "access model" in str(e).lower())
        ):
            raise HTTPException(
                status_code=401,
                detail="API Key inválida ou sem permissão para listar/acessar modelos.",
            )
        raise HTTPException(status_code=500, detail=detail_msg)


async def get_request_specific_gemini_client(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    requested_model_name: Optional[str] = None,
) -> GeminiClient:
    if not x_api_key:
        logger.warning("Cabeçalho X-API-Key não fornecido para get_request_specific_gemini_client.")
        raise HTTPException(status_code=401, detail="API Key não fornecida no cabeçalho X-API-Key.")
    try:
        model_to_use = (
            requested_model_name
            if requested_model_name and requested_model_name.strip()
            else get_gemini_model()
        )
        if model_to_use.startswith("models/"):
            model_to_use = model_to_use.replace("models/", "")

        client = GeminiClient(
            api_key=x_api_key, model_name=model_to_use
        )  # GeminiClient pode levantar ValueError ou ConnectionError
        logger.info(
            f"Cliente Gemini inicializado para a requisição com modelo: {client.model_name}."
        )
        return client
    except ValueError as ve:  # Erro na configuração do cliente (ex: modelo inválido, chave vazia)
        logger.error(f"Erro de valor ao criar cliente Gemini: {ve}", exc_info=True)
        raise HTTPException(
            status_code=400, detail=str(ve)
        )  # Cliente pode ter validado a chave aqui.
    except (
        ConnectionError
    ) as ce:  # Erro de conexão na inicialização do cliente (raro, mas possível)
        logger.critical(f"Erro de conexão ao criar cliente Gemini: {ce}", exc_info=True)
        raise HTTPException(status_code=503, detail=f"Erro ao configurar cliente da IA: {str(ce)}")
    except Exception as e:  # Outros erros inesperados na inicialização
        # Tenta identificar se é um erro de API Key da própria configuração do genai_core
        if "API key not valid" in str(e).lower() or "API_KEY_INVALID" in str(e).upper():
            logger.error(
                f"API Key inválida detectada na configuração do cliente Gemini: {e}", exc_info=True
            )
            raise HTTPException(status_code=401, detail="API Key do Gemini inválida.")
        logger.critical(f"Erro inesperado ao criar cliente Gemini: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao inicializar cliente da IA: {str(e)}"
        )


def _validate_project_zip_file(project_zip: UploadFile) -> None:
    if not project_zip.filename or not project_zip.filename.endswith(".zip"):
        logger.error(f"Upload inválido: {project_zip.filename}. Não é .zip ou sem nome.")
        raise HTTPException(status_code=400, detail="Arquivo .zip inválido ou ausente.")


async def _save_zip_and_extract_project_data(project_zip: UploadFile, temp_dir: str) -> str:
    temp_zip_path = os.path.join(
        temp_dir, project_zip.filename if project_zip.filename else "upload.zip"
    )
    with open(temp_zip_path, "wb") as tmp_file:
        content = await project_zip.read()
        tmp_file.write(content)
    logger.info(f"Arquivo .zip salvo temporariamente em: {temp_zip_path}")

    project_data_str = extract_project_data_from_zip(temp_zip_path, logger)
    if not project_data_str:
        logger.error("Falha ao extrair dados do ZIP.")
        raise HTTPException(status_code=500, detail="Não foi possível processar o arquivo .zip.")

    return project_data_str


def _build_badges_instructions(requested_badges: Optional[str]) -> str:
    if not requested_badges:
        return ""

    badges_list = [b.strip() for b in requested_badges.split(",") if b.strip()]
    if not badges_list:
        return ""

    return f"""

**Instruções Adicionais para Badges Solicitados:**
O usuário solicitou que a seção de badges (se aplicável ao nível de README) considere os seguintes tipos: {", ".join(badges_list)}.
* Ao gerar a seção de badges, use o `{{{{repo_link}}}}` (que você deve inferir das instruções gerais do usuário, se fornecido) para obter `{{{{usuario_inferido}}}}` e `{{{{projeto_inferido}}}}` e assim construir os URLs dos badges.
* Todos os badges devem usar `style=for-the-badge` (Ex: `![Nome Badge](https://img.shields.io/badge/exemplo-teste-blue?style=for-the-badge)`).
* Se o `{{{{repo_link}}}}` não estiver disponível, ou se um tipo de badge solicitado não for aplicável/inferível, omita-o discretamente.
* Se nenhum badge puder ser gerado com base nas informações e tipos solicitados, omita completamente a seção de badges do README.
* Exemplos de construção (adapte para os tipos solicitados e use `{{{{usuario_inferido}}}}/{{{{projeto_inferido}}}}`):
    - Para 'License': `https://img.shields.io/github/license/{{{{usuario_inferido}}}}/{{{{projeto_inferido}}}}`
    - Para 'Issues': `https://img.shields.io/github/issues/{{{{usuario_inferido}}}}/{{{{projeto_inferido}}}}`
    - Para 'Top Language': `https://img.shields.io/github/languages/top/{{{{usuario_inferido}}}}/{{{{projeto_inferido}}}}`
    - Para 'Last Commit': `https://img.shields.io/github/last-commit/{{{{usuario_inferido}}}}/{{{{projeto_inferido}}}}`
    - Para 'Contributors': `https://img.shields.io/github/contributors/{{{{usuario_inferido}}}}/{{{{projeto_inferido}}}}`
"""


def _build_generation_prompt(
    readme_level: str,
    project_data_str: str,
    repo_link: Optional[str],
    project_link: Optional[str],
    linkedin_link: Optional[str],
    requested_badges: Optional[str],
) -> str:
    prompt_map = {
        "simple": PROMPT_README_SIMPLE,
        "complete": PROMPT_README_COMPLETE,
        "moderate": PROMPT_README_MODERATE,
    }
    selected_prompt_template = prompt_map.get(readme_level, PROMPT_README_MODERATE)

    base_user_instructions = USER_LINKS_INSTRUCTIONS_TEMPLATE.format(
        repo_link=repo_link if repo_link else "Não fornecido",
        project_link=project_link if project_link else "Não fornecido",
        linkedin_link=linkedin_link if linkedin_link else "Não fornecido",
    )
    user_links_instructions_str = (
        f"{base_user_instructions}{_build_badges_instructions(requested_badges)}"
    )

    return selected_prompt_template.format(
        project_data=project_data_str,
        user_provided_links_instructions=user_links_instructions_str,
    )


def _map_connection_error_to_http_exception(error_message: str) -> HTTPException:
    user_friendly_detail = "Ocorreu um problema ao se comunicar com a API Gemini."

    original_error_match = re.search(
        r"Falha na comunicação com a API Gemini:\s*(.+)", error_message, re.DOTALL
    )
    original_error_str = original_error_match.group(1) if original_error_match else error_message

    if "400" in original_error_str and (
        "API key not valid" in original_error_str or "API_KEY_INVALID" in original_error_str.upper()
    ):
        user_friendly_detail = (
            "A API Key do Gemini fornecida é inválida. Verifique a chave e tente novamente."
        )
        return HTTPException(status_code=400, detail=user_friendly_detail)

    if "PermissionDenied" in original_error_str and (
        "permission to access model" in original_error_str.lower()
        or "User location is not supported" in original_error_str
    ):
        user_friendly_detail = "A API Key não tem permissão para usar o modelo Gemini selecionado ou sua região não é suportada. Verifique as configurações da sua chave e do modelo."
        return HTTPException(status_code=403, detail=user_friendly_detail)

    if (
        "429" in original_error_str
        and ("quota" in original_error_str.lower() or "ResourceExhausted" in original_error_str)
    ) or "RESOURCE_EXHAUSTED" in original_error_str.upper():
        detail_for_user = "Você excedeu sua cota atual da API Gemini. "
        if "migrate to" in original_error_str.lower():
            detail_for_user += "Considere verificar as opções de modelos ou planos com limites de cota mais altos. "
        else:
            detail_for_user += "Por favor, tente novamente mais tarde. "

        retry_match = re.search(
            r"retry_delay\s*{\s*seconds:\s*(\d+)\s*}", original_error_str, re.IGNORECASE
        )
        if retry_match:
            detail_for_user += (
                f"Você pode tentar novamente em aproximadamente {retry_match.group(1)} segundos. "
            )

        detail_for_user += "Consulte a seção 'Informações sobre Modelos Gemini' no rodapé da página ou visite https://ai.google.dev/gemini-api/docs/rate-limits."
        logger.warning(f"Cota da API Gemini excedida: {original_error_str}")
        return HTTPException(status_code=429, detail=detail_for_user)

    if (
        "500" in original_error_str
        or "Internal error" in original_error_str
        or "unavailable" in original_error_str.lower()
    ):
        user_friendly_detail = "A API Gemini reportou um erro interno ou está temporariamente indisponível. Tente novamente mais tarde."
        return HTTPException(status_code=502, detail=user_friendly_detail)

    return HTTPException(
        status_code=503,
        detail=f"Serviço indisponível: Falha na comunicação com a API Gemini. Detalhes técnicos: {original_error_str}",
    )


def _map_generate_readme_exception(exc: Exception) -> HTTPException:
    if isinstance(exc, ValueError):
        error_message = str(exc)
        logger.error(f"ValueError no endpoint: {error_message}", exc_info=True)
        if "PROMPT BLOQUEADO PELA IA" in error_message:
            user_detail = error_message.replace("PROMPT BLOQUEADO PELA IA (Safety): ", "").replace(
                "PROMPT BLOQUEADO PELA IA:", ""
            )
            return HTTPException(
                status_code=400,
                detail=f"Solicitação rejeitada pela IA devido a filtros de conteúdo/segurança: {user_detail.strip()}",
            )
        return HTTPException(
            status_code=400, detail=f"Erro nos dados da solicitação: {error_message}"
        )

    if isinstance(exc, ConnectionError):
        error_message = str(exc.args[0]) if exc.args else str(exc)
        logger.error(
            f"ConnectionError no endpoint (falha na comunicação com Gemini): {error_message}",
            exc_info=True,
        )
        return _map_connection_error_to_http_exception(error_message)

    if isinstance(exc, KeyError):
        logger.critical(
            f"KeyError ao formatar o prompt: '{exc}'. Placeholders no template: project_data, user_provided_links_instructions.",
            exc_info=True,
        )
        return HTTPException(
            status_code=500,
            detail=f"Erro de formatação interna do prompt: Chave '{str(exc)}' ausente. Isso é um bug no template do prompt.",
        )

    if isinstance(exc, HTTPException):
        logger.error(
            f"HTTPException pré-existente: {exc.status_code} - {exc.detail}",
            exc_info=True if exc.status_code >= 500 else False,
        )
        return exc

    logger.critical(
        f"Erro inesperado e não tratado no endpoint /api/generate-readme: {exc}", exc_info=True
    )
    return HTTPException(
        status_code=500,
        detail="Erro interno inesperado no servidor. Por favor, contate o suporte se o problema persistir.",
    )


@app.post("/api/generate-readme")
async def generate_readme_endpoint(
    project_zip: UploadFile = File(...),
    readme_level: str = Form("moderate"),
    repo_link: Optional[str] = Form(None),
    project_link: Optional[str] = Form(None),
    linkedin_link: Optional[str] = Form(None),
    requested_badges: Optional[str] = Form(None),
    gemini_model_select: Optional[str] = Form(None),
    x_api_key_header: Annotated[str | None, Header(alias="X-API-Key")] = None,
    rate_limit_status: None = Depends(rate_limit_checker),
):
    logger.info(
        f"Solicitação para /api/generate-readme: arquivo={project_zip.filename}, nivel={readme_level}, repo={repo_link}, projeto={project_link}, linkedin={linkedin_link}, badges={requested_badges}, modelo_selecionado='{gemini_model_select}'"
    )

    try:
        gemini_client = await get_request_specific_gemini_client(
            x_api_key_header, gemini_model_select
        )
        _validate_project_zip_file(project_zip)

        with tempfile.TemporaryDirectory() as temp_dir:
            project_data_str = await _save_zip_and_extract_project_data(project_zip, temp_dir)
            prompt = _build_generation_prompt(
                readme_level=readme_level,
                project_data_str=project_data_str,
                repo_link=repo_link,
                project_link=project_link,
                linkedin_link=linkedin_link,
                requested_badges=requested_badges,
            )

            logger.debug(
                f"Prompt selecionado (nível: {readme_level}, modelo: {gemini_client.model_name}). Tamanho aprox: {len(prompt):,} chars. Enviando para Gemini..."
            )
            readme_content = gemini_client.send_conversational_prompt(prompt)
            if not readme_content:
                logger.error(
                    "Falha ao gerar README: IA não retornou conteúdo, mas não levantou exceção."
                )
                raise HTTPException(
                    status_code=500, detail="Falha ao gerar README: IA não retornou conteúdo."
                )

            logger.info("README.md gerado com sucesso pela IA.")
            return JSONResponse(
                content={"filename": project_zip.filename, "readme_content": readme_content}
            )
    except Exception as exc:
        mapped_exception = _map_generate_readme_exception(exc)
        if mapped_exception is exc:
            raise
        raise mapped_exception from exc


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_root():
    html_file_path = os.path.join(project_root_dir, "index.html")
    if not os.path.exists(html_file_path):
        logger.error(f"Arquivo index.html não encontrado em {html_file_path}")
        return HTMLResponse(content="<h1>Erro: Frontend não encontrado.</h1>", status_code=404)
    try:
        with open(html_file_path, encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Erro ao ler index.html: {e}", exc_info=True)
        return HTMLResponse(content="<h1>Erro ao carregar a página.</h1>", status_code=500)


if __name__ == "__main__":
    logger.info("Iniciando Uvicorn localmente: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
