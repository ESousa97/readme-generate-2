# gerador_readme_ia_web/utils.py
import zipfile
import os
import logging
from typing import Optional

# O logger será obtido do chamador ou configurado globalmente
# logger = logging.getLogger(__name__) # Se precisar de um logger específico aqui

def extract_project_data_from_zip(zip_path: str, logger: logging.Logger, max_content_length_per_file: int = 7000, max_total_files_to_process: int = 70) -> Optional[str]:
    """
    Extrai a estrutura de pastas e o conteúdo de arquivos selecionados de um .zip.

    Args:
        zip_path: Caminho para o arquivo .zip.
        logger: Instância do logger para registrar mensagens.
        max_content_length_per_file: Máximo de caracteres a serem lidos de cada arquivo.
        max_total_files_to_process: Número máximo de arquivos cujo conteúdo será extraído.

    Returns:
        Uma string formatada com os dados do projeto ou None em caso de erro.
    """
    logger.debug(f"Iniciando extração de dados do arquivo ZIP: {zip_path}")
    project_data_parts = []
    files_processed_for_content = 0

    # Lista de extensões de código comuns e arquivos de configuração importantes
    # Ajuste esta lista conforme os tipos de projeto que você espera processar
    code_extensions = {
        '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rb', '.php',
        '.swift', '.kt', '.rs', '.html', '.css', '.scss', '.less', '.vue', '.jsx', '.tsx',
        '.md', '.txt', '.json', '.xml', '.yaml', '.yml', '.ini', '.cfg', '.toml',
        '.sh', '.bat', '.ps1', '.sql'
    }
    important_filenames = {
        'requirements.txt', 'package.json', 'pom.xml', 'build.gradle', 'setup.py',
        'dockerfile', 'docker-compose.yml', '.gitignore', 'license', 'contributing.md',
        'readme.md', 'makefile', 'cmakelists.txt', 'gemfile', 'composer.json',
        'webpack.config.js', 'babel.config.js', 'tsconfig.json', 'vite.config.js'
    }
    # Pastas a serem ignoradas (ex: node_modules, .git, __pycache__)
    ignored_dirs_patterns = {
        'node_modules/', '.git/', '__pycache__/', '.vscode/', '.idea/', 'venv/', 'env/',
        'build/', 'dist/', 'target/', '*.egg-info/'
    }


    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_infos = zf.infolist()
            
            project_data_parts.append("Estrutura do Projeto (Pastas e Arquivos Principais):\n")
            # Lista a estrutura de arquivos e diretórios
            # Pode ser simplificado para focar apenas em arquivos relevantes se a lista for muito grande
            for item in file_infos:
                # Lógica para pular arquivos em diretórios ignorados
                if any(item.filename.lower().startswith(pattern) or f"/{pattern}" in item.filename.lower() for pattern in ignored_dirs_patterns):
                    logger.debug(f"Ignorando item em diretório ignorado: {item.filename}")
                    continue
                
                # Adiciona à estrutura, indicando se é diretório
                project_data_parts.append(f"- {item.filename}{' (diretório)' if item.is_dir() else ''}\n")

            project_data_parts.append("\nConteúdo de Arquivos Relevantes (trechos):\n")

            # Filtra e processa arquivos para extração de conteúdo
            # Ordena para tentar processar arquivos mais importantes primeiro (ex: config, depois código)
            relevant_files_for_content = sorted(
                [
                    item for item in file_infos 
                    if not item.is_dir() and 
                    (os.path.splitext(item.filename)[1].lower() in code_extensions or \
                     os.path.basename(item.filename).lower() in important_filenames) and \
                    not any(item.filename.lower().startswith(pattern) or f"/{pattern}" in item.filename.lower() for pattern in ignored_dirs_patterns)
                ],
                key=lambda x: (0 if os.path.basename(x.filename).lower() in important_filenames else 1, x.filename)
            )


            for item in relevant_files_for_content:
                if files_processed_for_content >= max_total_files_to_process:
                    logger.info(f"Limite de {max_total_files_to_process} arquivos para extração de conteúdo atingido.")
                    project_data_parts.append(f"\n[AVISO: Análise de conteúdo limitada aos primeiros {max_total_files_to_process} arquivos relevantes.]\n")
                    break

                file_name = item.filename
                try:
                    # Limita o tamanho do arquivo a ser lido para evitar problemas com arquivos muito grandes
                    if item.file_size > 5 * 1024 * 1024: # Pula arquivos maiores que 5MB
                        logger.warning(f"Pulando arquivo '{file_name}' por ser muito grande: {item.file_size / (1024*1024):.2f} MB.")
                        project_data_parts.append(f"\n--- Arquivo: {file_name} (Pulado por ser muito grande) ---\n")
                        continue

                    with zf.open(item) as file_in_zip:
                        file_bytes = file_in_zip.read()
                        file_content = "[Erro na decodificação do conteúdo]"
                        try:
                            # Tenta decodificar como UTF-8, fallback para latin-1
                            file_content = file_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                file_content = file_bytes.decode('latin-1', errors='ignore')
                                logger.warning(f"Arquivo '{file_name}' decodificado como latin-1 após falha no UTF-8.")
                            except Exception as e_decode_latin:
                                logger.error(f"Não foi possível decodificar o arquivo '{file_name}' como UTF-8 ou latin-1: {e_decode_latin}")
                        
                        # Trunca o conteúdo se for muito longo
                        truncated_info = ""
                        if len(file_content) > max_content_length_per_file:
                            file_content = file_content[:max_content_length_per_file]
                            truncated_info = f"\n[CONTEÚDO TRUNCADO em {max_content_length_per_file} caracteres]"
                        
                        project_data_parts.append(f"\n--- Arquivo: {file_name} ---\n{file_content}{truncated_info}\n")
                        files_processed_for_content += 1

                except Exception as e_file:
                    logger.warning(f"Erro ao ler ou processar o arquivo '{file_name}' dentro do ZIP: {e_file}", exc_info=True)
                    project_data_parts.append(f"\n--- Arquivo: {file_name} ---\n[Erro na leitura do arquivo: {e_file}]\n")
            
            if not relevant_files_for_content:
                project_data_parts.append("[Nenhum arquivo de código ou configuração relevante encontrado para extrair conteúdo.]\n")

            logger.info(f"Extração de dados do ZIP concluída. {files_processed_for_content} arquivos tiveram seu conteúdo processado.")
            return "".join(project_data_parts)

    except zipfile.BadZipFile:
        logger.error(f"Arquivo ZIP inválido ou corrompido: {zip_path}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao processar o arquivo ZIP {zip_path}: {e}", exc_info=True)
        return None
