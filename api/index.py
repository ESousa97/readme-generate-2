# api/index.py
import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Annotated, Optional
import tempfile

import sys
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(current_file_dir)
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from gerador_readme_ia_web.config import get_gemini_model, APP_NAME, APP_AUTHOR
# PROMPT_README_GENERATION será substituído pela lógica de seleção de prompt
from gerador_readme_ia_web.constants_web import (
    PROMPT_README_SIMPLE, 
    PROMPT_README_MODERATE, 
    PROMPT_README_COMPLETE
)
from gerador_readme_ia_web.gemini_client_web import GeminiClient
from gerador_readme_ia_web.utils import extract_project_data_from_zip
from gerador_readme_ia_web.logger_setup_web import setup_logging

logger = setup_logging(f"{APP_NAME}.api", app_author=APP_AUTHOR, debug=True, is_web_app=True)
logger.info(f"Sistema Operacional detectado (os.name): {os.name}")

app = FastAPI(
    title="Gerador de README.md API",
    description="API para gerar README.md com níveis de detalhe e informações opcionais.",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.path.join(project_root_dir, "static")), name="static")

async def get_request_specific_gemini_client(x_api_key: Annotated[str | None, Header()] = None) -> GeminiClient:
    if not x_api_key:
        logger.warning("Cabeçalho X-API-Key não fornecido.")
        raise HTTPException(status_code=401, detail="API Key não fornecida no cabeçalho X-API-Key.")
    try:
        model_name = get_gemini_model()
        client = GeminiClient(api_key=x_api_key, model_name=model_name)
        logger.info(f"Cliente Gemini inicializado para a requisição com modelo: {model_name}.")
        return client
    except Exception as e: # Captura mais genérica para erros de inicialização do cliente
        logger.critical(f"Erro ao criar cliente Gemini: {e}", exc_info=True)
        raise HTTPException(status_code=503, detail=f"Erro ao configurar cliente da IA: {str(e)}")


@app.post("/api/generate-readme")
async def generate_readme_endpoint(
    project_zip: UploadFile = File(...),
    readme_level: str = Form("moderate"), # Valor padrão 'moderate'
    repo_link: Optional[str] = Form(None),
    linkedin_link: Optional[str] = Form(None),
    gemini_client: GeminiClient = Depends(get_request_specific_gemini_client)
):
    logger.info(f"Solicitação para /api/generate-readme: arquivo={project_zip.filename}, nivel={readme_level}, repo={repo_link}, linkedin={linkedin_link}")

    if not project_zip.filename or not project_zip.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Arquivo .zip inválido ou ausente.")

    temp_zip_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip", prefix="upload_") as tmp_file:
            content = await project_zip.read()
            tmp_file.write(content)
            temp_zip_path = tmp_file.name
        logger.info(f"Arquivo .zip salvo temporariamente em: {temp_zip_path}")

        project_data_str = extract_project_data_from_zip(temp_zip_path, logger)
        if not project_data_str:
            raise HTTPException(status_code=500, detail="Não foi possível processar o arquivo .zip.")
        
        # Selecionar o prompt com base no nível
        if readme_level == "simple":
            selected_prompt_template = PROMPT_README_SIMPLE
        elif readme_level == "complete":
            selected_prompt_template = PROMPT_README_COMPLETE
        else: # Padrão para moderado
            selected_prompt_template = PROMPT_README_MODERATE
        
        # Montar o prompt final, incorporando links se fornecidos
        # Adicionaremos uma seção ao início do project_data para os links
        additional_context = ""
        if repo_link:
            additional_context += f"\n\nInformações Adicionais Fornecidas pelo Usuário:\n- Link do Repositório do Projeto: {repo_link}\n"
        if linkedin_link:
            if not additional_context: # Se repo_link não foi fornecido
                 additional_context += f"\n\nInformações Adicionais Fornecidas pelo Usuário:\n"
            additional_context += f"- Link do Perfil LinkedIn do Autor/Contato Principal: {linkedin_link}\n"
        
        # Instrução para a IA usar esses links
        if additional_context:
            additional_context += "\nInstrução: Utilize as 'Informações Adicionais Fornecidas pelo Usuário' acima para enriquecer as seções apropriadas do README, como 'Badges' (usando o link do repositório), 'Autores/Contato', ou para inferir o nome do autor/projeto. NÃO liste esta seção 'Informações Adicionais Fornecidas pelo Usuário' diretamente no README final.\n"

        final_project_data = additional_context + project_data_str
        
        prompt = selected_prompt_template.format(project_data=final_project_data)
        logger.debug(f"Prompt selecionado (nível: {readme_level}). Enviando para Gemini...")
        
        readme_content = gemini_client.send_conversational_prompt(prompt)

        if readme_content:
            logger.info("README.md gerado com sucesso pela IA.")
            return JSONResponse(content={"filename": project_zip.filename, "readme_content": readme_content})
        else:
            raise HTTPException(status_code=500, detail="Falha ao gerar README: IA não retornou conteúdo ou prompt foi bloqueado.")

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.critical(f"Erro inesperado: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    finally:
        if temp_zip_path and os.path.exists(temp_zip_path):
            try:
                os.remove(temp_zip_path)
                logger.info(f"Arquivo temporário {temp_zip_path} removido.")
            except Exception as e_rm:
                logger.error(f"Erro ao remover {temp_zip_path}: {e_rm}", exc_info=True)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_root():
    html_file_path = os.path.join(project_root_dir, "index.html")
    if not os.path.exists(html_file_path):
        return HTMLResponse(content="<h1>Erro: Frontend não encontrado.</h1>", status_code=404)
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    logger.info("Iniciando Uvicorn localmente: http://127.0.0.1:8000")
    uvicorn.run("api.index:app", host="127.0.0.1", port=8000, reload=True)
