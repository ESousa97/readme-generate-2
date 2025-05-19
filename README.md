# Gerador de README.md com IA

**Gere READMEs profissionais e completos para seus projetos com a força da IA Gemini!**

[![Status da Build](https://img.shields.io/github/actions/workflow/status/USUARIO/REPO/main.yml?branch=main&style=for-the-badge)](https://github.com/USUARIO/REPO/actions)
[![Última Release](https://img.shields.io/github/v/release/USUARIO/REPO?style=for-the-badge)](https://github.com/USUARIO/REPO/releases)
[![Licença](https://img.shields.io/github/license/USUARIO/REPO?style=for-the-badge)](LICENSE.md)
[![Linguagem Principal](https://img.shields.io/github/languages/top/USUARIO/REPO?style=for-the-badge)](https://github.com/USUARIO/REPO)
[![Contribuições Bem-vindas](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)
[![Issues Abertas](https://img.shields.io/github/issues/USUARIO/REPO?style=for-the-badge)](https://github.com/USUARIO/REPO/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/USUARIO/REPO?style=for-the-badge)](https://github.com/USUARIO/REPO/pulls)
[![Tamanho do Repositório](https://img.shields.io/github/repo-size/USUARIO/REPO?style=for-the-badge)](https://github.com/USUARIO/REPO)


## Descrição Detalhada

Este projeto fornece uma API e uma interface web simples para gerar arquivos `README.md` para projetos de software utilizando a IA Gemini.  Basta fornecer um arquivo `.zip` contendo o código-fonte do seu projeto, e a API retornará um `README.md` bem formatado e informativo, contendo informações como a estrutura do projeto, tecnologias utilizadas, instruções de instalação e muito mais.  Isso facilita a documentação de seus projetos e a colaboração com outros desenvolvedores. O público-alvo são desenvolvedores que buscam automatizar a criação de documentação e facilitar a publicação de seus projetos open source ou internos.

## 🚧 Status do Projeto

Em Desenvolvimento Ativo


## Visualização

A aplicação web possui uma interface intuitiva e amigável.  Para uma demonstração visual, acesse [a aplicação online](URL_DA_APLICAÇÃO_ONLINE).  Uma captura de tela da interface será adicionada em breve.


## ✨ Funcionalidades Principais

- 🚀 Gera READMEs completos e profissionais com base no código do seu projeto.
- 🤖 Utiliza a IA Gemini para gerar descrições precisas e concisas.
- 📦 Aceita arquivos `.zip` contendo o código-fonte do projeto.
- 📄 Retorna um `README.md` formatado em Markdown.
- 🌐 Interface web amigável e intuitiva.
- 🔑 Autenticação segura via API Key.


## 🛠️ Tecnologias Utilizadas

| Categoria  | Tecnologias                               |
|------------|-------------------------------------------|
| Backend    | Python (FastAPI), Google Gemini           |
| Frontend   | HTML, JavaScript, Tailwind CSS            |
| Ferramentas | Docker, GitHub Actions, Vercel            |


## 📂 Estrutura do Projeto

```
.
├── api/                     # API FastAPI para geração do README
│   └── index.py             # Ponto de entrada da API
├── gerador_readme_ia_web/   # Módulos principais do gerador de README
│   ├── config.py            # Configurações da aplicação
│   ├── constants_web.py     # Constantes para a aplicação web
│   ├── gemini_client_web.py # Cliente para interação com a API Gemini
│   ├── logger_setup_web.py  # Configuração de logging
│   ├── utils.py             # Funções utilitárias
│   └── __init__.py
├── index.html               # Página web principal
├── requirements.txt         # Dependências Python
├── static/                  # Arquivos estáticos (JS, CSS)
│   └── script.js            # Script JavaScript da interface web
└── vercel.json              # Configuração do deployment para Vercel
```


## 📋 Pré-requisitos

- Python (>=3.9)
- Node.js (para build do frontend, opcional)
- Conta no Google Cloud com acesso à API Gemini (para uso da IA)
- Docker (recomendado para desenvolvimento local)


## 🚀 Guia de Início Rápido (Getting Started)

1. **Clone o repositório:**
   ```bash
   git clone URL_DO_SEU_REPOSITORIO_AQUI
   cd gerador-readme-ia
   ```

2. **Crie e ative um ambiente virtual (Python):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
    * Crie um arquivo `.env` na raiz do projeto (copie de `.env.example` se existir).
    * Defina a sua `GEMINI_API_KEY` no arquivo `.env`.

5. **Execute a aplicação (modo de desenvolvimento):**
   ```bash
   uvicorn api.index:app --reload
   ```

6. Acesse `http://localhost:8000` no seu navegador.


## ⚙️ Uso e Comandos Detalhados

- **Rodar em modo de produção:**  (Instruções específicas para o seu ambiente de produção serão adicionadas.)
- **Build do Frontend:** (Se necessário, adicione instruções para construir os arquivos estáticos.)


## 🔧 Configuração Avançada

- `GEMINI_API_KEY`: (Obrigatório) Sua API Key do Google Gemini.
- `GEMINI_MODEL_NAME`: (Opcional) Nome do modelo Gemini a ser usado (padrão: `gemini-1.5-flash-latest`).  Veja a documentação da API Gemini para opções.


## 🧪 Testes

(Instruções para executar os testes serão adicionadas.)


## 🚢 Deployment (Implantação)

Este projeto é configurado para implantação no Vercel usando o arquivo `vercel.json`. Veja a documentação do Vercel para detalhes sobre o deployment.


## 🤝 Como Contribuir

Leia nosso [Guia de Contribuição](CONTRIBUTING.md) para mais detalhes.


## 📜 Licença

Distribuído sob a Licença MIT. Veja `LICENSE.md` para mais informações.


## 👥 Autores e Agradecimentos

(A ser completado)


## 📞 Contato e Suporte

Abra uma [Issue no GitHub](URL_DO_REPOSITORIO/issues/new/choose) para reportar bugs ou solicitar suporte.
