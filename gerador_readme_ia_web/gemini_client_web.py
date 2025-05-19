# gerador_readme_ia_web/ia_client/gemini_client_web.py
import google.generativeai as genai
import logging
from typing import Optional

# Importa o nome da aplicação das configurações web
from .config import APP_NAME

# Logger específico para este módulo
# O logger principal será configurado pelo logger_setup_web.py
logger = logging.getLogger(f"{APP_NAME}.gemini_client_web")

class GeminiClient:
    def __init__(self, api_key: str, model_name: str):
        logger.info(f"Inicializando GeminiClient com modelo '{model_name}'.")
        if not api_key:
            logger.error("API Key não fornecida para o GeminiClient.")
            raise ValueError("API Key é obrigatória para inicializar o GeminiClient.")
        if not model_name:
            logger.error("Nome do modelo não fornecido para o GeminiClient.")
            raise ValueError("Nome do modelo é obrigatório para inicializar o GeminiClient.")

        try:
            genai.configure(api_key=api_key)
            
            # Configurações de segurança padrão (ajuste conforme necessário)
            default_safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
            
            self.model = genai.GenerativeModel(
                model_name=model_name,
                safety_settings=default_safety_settings
            )
            self.model_name = model_name
            logger.info(f"GeminiClient inicializado com sucesso para o modelo '{model_name}'.")
        except Exception as e:
            logger.critical(f"Exceção crítica durante a inicialização do modelo Gemini '{model_name}': {e}", exc_info=True)
            raise ConnectionError(
                f"Não foi possível inicializar o modelo Gemini '{model_name}'. "
                "Verifique o nome do modelo, a API Key, as configurações de segurança e sua conexão."
            ) from e

    def send_conversational_prompt(self, prompt_text: str) -> Optional[str]:
        logger.info(f"Enviando prompt para o modelo: {self.model_name}. Tamanho (aprox): {len(prompt_text):,} caracteres.")
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=0.6, # Ajuste a temperatura conforme necessário
                # max_output_tokens=8192, # Descomente e ajuste se precisar limitar o tamanho da resposta
            )
            
            logger.debug("Chamando model.generate_content...")
            response = self.model.generate_content(
                contents=prompt_text,
                generation_config=generation_config
            )
            # logger.debug(f"Resposta bruta do Gemini: {response}") # Pode ser muito verboso

            if response.text:
                logger.info("Resposta textual recebida do Gemini.")
                return response.text
            elif hasattr(response, 'parts') and response.parts:
                # Para alguns modelos ou respostas mais complexas, o texto pode estar em 'parts'
                full_response_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
                if full_response_text:
                    logger.info("Resposta textual (via response.parts) recebida do Gemini.")
                    return full_response_text
            
            # Verifica se o prompt foi bloqueado
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                block_reason_str = str(response.prompt_feedback.block_reason)
                logger.error(f"Solicitação bloqueada pelo Gemini. Razão: {block_reason_str}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        logger.error(f"  Safety Rating: Category={rating.category}, Probability={rating.probability}")
                raise ValueError(f"PROMPT BLOQUEADO PELA IA. Razão: {block_reason_str}")
            
            logger.warning("Resposta do Gemini não continha conteúdo textual esperado e não foi explicitamente bloqueada.")
            return None # Ou raise ValueError("Resposta inesperada da IA.")

        except ValueError as ve: # Captura o erro de prompt bloqueado
            logger.error(f"Erro de valor durante chamada à API Gemini (modelo {self.model_name}): {ve}", exc_info=True)
            raise # Re-levanta para ser tratado pelo endpoint da API
        except Exception as e:
            logger.error(f"Erro inesperado durante chamada à API Gemini (modelo {self.model_name}): {e}", exc_info=True)
            raise ConnectionError(f"Falha na comunicação com a API Gemini: {str(e)}") from e


    def test_connection(self) -> bool:
        logger.info(f"Testando conexão com o modelo Gemini '{self.model_name}'...")
        try:
            # Envia um prompt simples para teste
            response = self.model.generate_content(
                "Olá! Este é um teste de conexão.",
                generation_config=genai.types.GenerationConfig(temperature=0.9, candidate_count=1)
            )
            # logger.debug(f"Resposta do teste de conexão: {response}") # Pode ser verboso
            if response.text:
                logger.info(f"Teste de conexão com '{self.model_name}' bem-sucedido. Resposta recebida.")
                return True
            elif hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                logger.error(f"Teste de conexão falhou: prompt de teste bloqueado. Razão: {response.prompt_feedback.block_reason}")
                # Não levanta exceção aqui, apenas retorna False, o chamador decide o que fazer.
                return False
            else:
                logger.warning(f"Teste de conexão com '{self.model_name}': resposta vazia, mas sem erro de API. Considerando OK.")
                return True # Alguns modelos podem retornar vazio para prompts muito simples
        except Exception as e:
            logger.error(f"Exceção crítica durante o teste de conexão com '{self.model_name}': {e}", exc_info=True)
            # Não levanta exceção aqui, apenas retorna False
            return False

    def close(self):
        """
        Método para 'fechar' o cliente. Para o SDK do Gemini, não há uma conexão persistente
        para fechar explicitamente, mas este método pode ser usado para qualquer limpeza futura.
        """
        logger.info(f"Cliente Gemini ({self.model_name}) 'fechado'. Nenhuma ação específica necessária para o SDK atual.")

