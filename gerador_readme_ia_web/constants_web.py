# gerador_readme_ia_web/constants_web.py

# ATENÇÃO: Este é o template para as instruções sobre os links do usuário.
# Ele usa {repo_link}, {project_link} e {linkedin_link} como placeholders para o Python formatar.
# As chaves {{usuario_inferido}} e {{projeto_inferido}} são para a IA interpretar.
USER_LINKS_INSTRUCTIONS_TEMPLATE = """

**Contexto Adicional Fornecido pelo Usuário (para uso interno da IA, NÃO listar no README):**
* Link do Repositório do Projeto (GitHub, GitLab, etc.): {repo_link}
* Link do Projeto (Demonstração, Produção, Site Oficial, etc.): {project_link}
* Link do Perfil LinkedIn do Autor/Contato Principal: {linkedin_link}

**Instruções Cruciais para Uso dos Links (Aplicar em todos os níveis de README):**
1.  **NÃO** liste esta seção "Contexto Adicional Fornecido pelo Usuário" no README final.
2.  **Link do Repositório:**
    * Se fornecido (diferente de "Não fornecido"), use-o para:
        * Inferir o nome do usuário/organização e o nome do projeto (ex: de `https://github.com/usuario/projeto`, inferir `usuario/projeto`).
        * Construir URLs para badges (ex: `![License](https://img.shields.io/github/license/{{usuario_inferido}}/{{projeto_inferido}})`).
        * Criar links diretos para Issues, Pull Requests, e o próprio repositório nas seções apropriadas (ex: Contribuição, Clonagem).
        * Mencionar o comando de clone correto: `git clone {repo_link}`.
    * Se "Não fornecido", use placeholders genéricos como `URL_DO_REPOSITORIO_AQUI` ou `USUARIO/PROJETO` onde necessário.
3.  **Link do Projeto:**
    * Se fornecido (diferente de "Não fornecido"), use-o para:
        * Criar um link direto para o projeto em uma seção como "Como Acessar o Projeto", "Demonstração Ao Vivo", "Deploy", ou "Link Principal do Projeto". O nome da seção pode variar conforme o contexto do projeto.
        * Se o nível do README for 'Moderado' ou 'Completo', considere adicioná-lo próximo à descrição ou em uma seção de visualização/acesso.
        * Exemplo: `[Acesse o Projeto Aqui]({project_link})` ou `[Veja a Demo Online]({project_link})`.
    * Se "Não fornecido", omita qualquer menção a este link específico. Não use placeholders para este link se ele não for fornecido.
4.  **Link do LinkedIn:**
    * Se fornecido (diferente de "Não fornecido"), use-o para:
        * Enriquecer a seção "Autores" ou "Contato", vinculando ao perfil do autor.
        * Inferir o nome do autor, se possível.
    * Se "Não fornecido", omita menções diretas ao LinkedIn do autor ou use um placeholder genérico se a seção de autor for mantida.
"""

# ATENÇÃO: Este é o cabeçalho base para todos os prompts.
# Ele usa {project_data} e {user_provided_links_instructions} como placeholders para o Python formatar.
PROMPT_README_BASE_HEADER = """
Analise os dados do projeto fornecidos (estrutura de diretórios e conteúdo de arquivos selecionados de um arquivo .zip) e as instruções sobre links do usuário para gerar um README.md em Português do Brasil.

**Dados do Projeto (extraídos do arquivo .zip):**
{project_data}
{user_provided_links_instructions}

**Formato Final do Output:**
* O output DEVE ser **apenas** o conteúdo completo do arquivo README.md.
* Formate todo o conteúdo utilizando Markdown padrão do GitHub (GFM).
* Não inclua nenhuma introdução, conclusão, comentários ou metadados seus antes ou depois do conteúdo do README.
---
"""

# NÍVEL 1: SIMPLES (Foco: Essencial para Desenvolvedor Experiente)
PROMPT_README_SIMPLE = PROMPT_README_BASE_HEADER + """
**Persona da IA:** Você é um Desenvolvedor de Software Sênior (5+ anos de experiência) criando um README para outros desenvolvedores experientes. A documentação deve ser minimalista, funcional e direta ao ponto.

**Objetivo:** Gerar um README.md conciso e funcional, cobrindo **apenas** os aspectos cruciais para que outro desenvolvedor possa entender o propósito do projeto e executá-lo rapidamente. Evite seções supérfluas.

**Seções Essenciais a Incluir (se inferível e aplicável):**
1.  **Título do Projeto:** Curto e claro. (Inferir do nome do repositório se possível, usando as instruções de links).
2.  **Descrição Curta:** (1-2 frases sobre o que o projeto faz).
3.  **(Opcional, se fornecido) Link do Projeto:** Se o `{{project_link}}` foi fornecido, inclua um link direto para ele de forma concisa. Ex: `[Acesse o Projeto]({{project_link}})`.
4.  **Tecnologias Utilizadas:** Lista simples das principais tecnologias (ex: Python, React, Docker).
5.  **Pré-requisitos:** Apenas os absolutamente necessários para rodar.
6.  **Como Instalar e Configurar:** Passos mínimos e essenciais.
    * Use o `{{repo_link}}` fornecido no comando `git clone`. Se não houver, use `git clone URL_DO_PROJETO_AQUI`.
    * Comandos de instalação de dependências (ex: `pip install -r requirements.txt`).
    * Configuração mínima (ex: `cp .env.example .env`, se aplicável, explique em uma linha).
7.  **Como Executar:** Comando principal para iniciar a aplicação (ex: `python main.py`).
8.  **(Opcional e Conciso) Licença:** Se um arquivo LICENSE for encontrado, mencione o tipo. Use o `{{repo_link}}` para criar um badge de licença simples se possível.

**Estilo e Restrições:**
* Linguagem técnica, direta e objetiva.
* Use cabeçalhos Markdown (`##`, `###`) para cada seção.
* Mínimo de formatação extra. Sem emojis.
* Badges: No máximo 1 ou 2 (ex: licença), usando o `{{repo_link}}` conforme instruído (a IA deve inferir `{{usuario_inferido}}`/`{{projeto_inferido}}` a partir do `{{repo_link}}`).
* Evite seções como "Status do Projeto", "Funcionalidades Detalhadas", "Estrutura do Projeto", "Contribuição", "Autores", a menos que uma informação crítica do projeto exija uma menção brevíssima.
"""

# NÍVEL 2: MODERADO (Foco: Documentação Profissional e Informativa)
PROMPT_README_MODERATE = PROMPT_README_BASE_HEADER + """
**Persona da IA:** Você é um Engenheiro de Software experiente (10+ anos) e Technical Writer, focado em criar READMEs claros, bem estruturados e informativos para uma audiência técnica geral.

**Objetivo:** Gerar um README.md profissional, bem organizado e visualmente agradável, que forneça uma compreensão abrangente do projeto, suas funcionalidades e como utilizá-lo.

**Seções Mandatórias e Sugeridas (adapte conforme os dados do projeto e use os links fornecidos, a IA deve inferir {{usuario_inferido}} e {{projeto_inferido}} do {{repo_link}} e utilizar {{project_link}} e {{linkedin_link}} quando necessário):**
1.  **Título do Projeto:** Impactante e descritivo. (Inferir do `{{repo_link}}`).
    * **Slogan/Tagline:** (Opcional, 1-2 linhas).
2.  **Badges (Shields.io):**
    * Agrupados no topo. Use o `{{repo_link}}` (ex: `usuario/projeto` - inferido pela IA) para construir os URLs dos badges (ex: Build, Versão, Licença, Issues Abertas, Linguagem Principal). Use `style=for-the-badge`.
    * Exemplo: `![GitHub issues](https://img.shields.io/github/issues/{{usuario_inferido}}/{{projeto_inferido}}?style=for-the-badge)`
3.  **Descrição Detalhada:** (1-3 parágrafos) O que o projeto faz, o problema que resolve, principais diferenciais.
4.  **Status do Projeto:** (Ex: `🚧 Em Desenvolvimento`, `✅ Estável`, ` manutenção apenas`).
5.  **(Opcional) Link Principal do Projeto / Demonstração:** Se o `{{project_link}}` foi fornecido, crie uma seção clara ou um link proeminente para ele. Ex: `## 🚀 Acesso ao Projeto` ou `[Veja a Demo Online!]({{project_link}})`.
6.  **(Opcional) Visualização:** Indique onde uma captura de tela ou GIF seria útil (ex: ``). Se `{{project_link}}` aponta para uma demo, mencione isso.
7.  **✨ Funcionalidades Principais (Features):** Lista com *bullet points*, descrições concisas.
8.  **🛠️ Tecnologias Utilizadas (Tech Stack):** Lista organizada das principais tecnologias.
9.  **📂 Estrutura do Projeto (Opcional):** Breve visão geral das pastas/arquivos mais importantes, se relevante para o entendimento.
10. **📋 Pré-requisitos:** Lista clara de dependências de software, ferramentas e versões.
11. **🚀 Guia de Início Rápido (Getting Started):**
    * Clonagem: `git clone {{repo_link}}` (ou placeholder se não fornecido).
    * Instalação de dependências.
    * Configuração essencial (variáveis de ambiente, etc.).
    * Comando para executar.
12. **⚙️ Uso (Exemplos):** (Opcional) Exemplos básicos de como usar o projeto ou suas principais funcionalidades. Se `{{project_link}}` for uma demo interativa, referencie-a.
13. **🤝 Como Contribuir (Contributing):**
    * Breves instruções ou link para `CONTRIBUTING.md` (se existir).
    * Incentive contribuições. Use o `{{repo_link}}` para criar links para Issues e Pull Requests.
14. **📜 Licença:** Indique claramente a licença. Se `LICENSE` encontrado, mencione. Adicione badge.
15. **👥 Autores/Contato:**
    * Mencione o(s) autor(es) principal(is).
    * Se o `{{linkedin_link}}` foi fornecido, adicione um link para o perfil do autor.

**Estilo:**
* Claro, conciso e profissional.
* Use emojis de forma sutil para melhorar a legibilidade das seções.
* Blocos de código bem formatados para comandos.
"""

# NÍVEL 3: COMPLETO (Foco: Documentação Exaustiva e Técnica)
PROMPT_README_COMPLETE = PROMPT_README_BASE_HEADER + """
**Persona da IA:** Você é um Arquiteto de Software e Pesquisador experiente (PhD, 11+ anos), elaborando uma documentação técnica de referência, profunda e abrangente, para um projeto complexo. O público inclui tanto desenvolvedores experientes quanto potenciais colaboradores de pesquisa. Seu objetivo é gerar um README.md que não apenas liste informações, mas que explique, justifique e contextualize, tornando o projeto compreensível em profundidade.

**Objetivo:** Produzir um README.md exaustivo, academicamente rigoroso (quando aplicável ao projeto) e pedagogicamente estruturado. Deve ser a principal fonte de conhecimento sobre o projeto, facilitando a compreensão profunda, a colaboração e a extensão. Siga a estrutura e o nível de detalhe exemplificados pelas seções abaixo, adaptando o conteúdo especificamente ao projeto analisado.

**Diretrizes e Foco:**
* **Profundidade Analítica:** Vá além da simples listagem. Explique o "porquê" por trás das escolhas de design, arquitetura e tecnologia. Analise trade-offs.
* **Rigor e Precisão:** Utilize terminologia técnica correta e seja preciso nas descrições.
* **Clareza Estrutural Avançada:** Utilize tabelas, listas detalhadas, blocos de código bem formatados e sugira onde diagramas (Mermaid ou ASCII) seriam benéficos para ilustrar conceitos complexos.
* **Obrigatoriedade das Seções:** É crucial que você tente gerar conteúdo substancial e detalhado para TODAS as seções listadas abaixo. Cada seção deve ser preenchida com informações específicas do projeto analisado. Se, após uma análise profunda, uma seção específica não for de todo aplicável (ex: 'Publicações' para um projeto que não tem nenhuma), indique explicitamente "Não aplicável a este projeto neste momento" ou omita-a com uma breve justificativa interna se absolutamente necessário, mas a prioridade é a completude exaustiva.

**Seções Detalhadas (adapte o conteúdo de cada seção ao projeto analisado, mantendo a profundidade e o formato sugerido. Gere explicações ricas e detalhadas):**

1.  **Título do Projeto e Slogan Filosófico:**
    * Gere um título formal e descritivo para o projeto.
    * Crie um slogan conciso e impactante que reflita a visão, o propósito central ou o principal benefício do projeto. (Inferir nome do projeto do `{{repo_link}}` se possível e relevante).

2.  **Abstract (Resumo Técnico):** (1-2 parágrafos substanciais)
    * Elabore um resumo técnico denso e informativo, como um abstract de artigo científico.
    * Deve cobrir:
        * **Contexto:** O domínio geral e a importância do problema que o projeto aborda.
        * **Problema:** A lacuna específica ou desafio que o projeto visa resolver.
        * **Solução Proposta:** A essência da abordagem do projeto para resolver o problema.
        * **Metodologia Principal:** As técnicas, algoritmos ou arquiteturas chave empregadas.
        * **Resultados Esperados/Alcançados:** Os principais resultados ou impactos do projeto.
        * **Contribuição/Inovação:** A singularidade ou o avanço que o projeto representa.

3.  **Badges Abrangentes:**
    * Inclua uma coleção abrangente e relevante de badges (Shields.io) que forneçam informações rápidas sobre o estado e características do projeto.
    * Utilize o `{{repo_link}}` extensivamente para inferir `{{usuario_inferido}}` e `{{projeto_inferido}}` para construir os URLs dos badges.
    * Tipos de badges a considerar (inclua todos que forem aplicáveis e inferíveis): Status da Build/CI, Licença, Linguagem Principal, Versão Mais Recente (se aplicável), Tamanho do Repositório, Último Commit, Número de Contribuidores, Issues Abertas, Pull Requests Abertas, Test Coverage, Qualidade de Código (ex: CodeClimate, SonarQube), Segurança (ex: Snyk, Dependabot), Downloads (se aplicável), Atividade Recente.
    * Todos os badges devem usar `style=for-the-badge`.

4.  **Sumário (Table of Contents):**
    * Gere um sumário detalhado e navegável, com links funcionais para todas as principais seções e subseções do README.

5.  **Introdução e Motivação:** (Múltiplos parágrafos)
    * Forneça uma contextualização detalhada e aprofundada do problema que o projeto aborda. Por que este problema é significativo?
    * Discuta as limitações ou deficiências de soluções existentes ou abordagens anteriores, se aplicável.
    * Apresente a proposta de valor única e inovadora do projeto de forma clara. Quais são os principais diferenciais?
    * Explique a motivação central para o desenvolvimento do projeto, incluindo os objetivos de longo prazo e o impacto desejado.

6.  **🔗 Link Principal / Acesso ao Projeto:**
    * Se o `{{project_link}}` for fornecido pelo usuário, crie uma seção dedicada e proeminente (ex: "🚀 Acesso ao Projeto", "🔗 Demonstração Online e Recursos").
    * Forneça uma breve descrição do que o link oferece (ex: demo interativa, documentação completa, site oficial, acesso à plataforma, artefatos de design).
    * Se não fornecido, omita esta seção.

7.  **Arquitetura do Sistema:**
    * Descreva detalhadamente os componentes arquiteturais principais do sistema/software, seus módulos, suas interações e as responsabilidades de cada um.
    * **Inclua um diagrama de arquitetura** (use Mermaid.js ou arte ASCII) que ilustre claramente os componentes e o fluxo de dados/controle entre eles. Exemplo de estrutura Mermaid a ser preenchida:
      \`\`\`mermaid
      graph TD
          A[Componente A] --> B(Componente B);
          B --> C{{Subsistema C}};
          C --> D[Banco de Dados];
          A --> E[Serviço Externo X];
      \`\`\`
    * Explique o diagrama, detalhando cada componente e interação.
    * Discuta as decisões arquiteturais chave (ex: escolha de padrões como microserviços, monolítico, event-driven; camadas da aplicação) e justifique-as, incluindo os trade-offs considerados.

8.  **Decisões de Design Chave:**
    * Apresente e justifique as decisões de design técnico mais importantes tomadas durante o desenvolvimento.
    * Isso pode incluir: escolha de linguagens de programação específicas, frameworks, bibliotecas importantes, algoritmos críticos, estruturas de dados fundamentais, protocolos de comunicação, etc.
    * Para cada decisão, explique o "porquê": quais foram os requisitos ou restrições que levaram a essa escolha? Quais alternativas foram consideradas e por que foram descartadas?

9.  **✨ Funcionalidades Detalhadas (com Casos de Uso):**
    * Liste e descreva cada funcionalidade principal do projeto de forma exaustiva.
    * Para cada funcionalidade:
        * Explique seu propósito e como ela contribui para os objetivos gerais do projeto.
        * Forneça exemplos claros de casos de uso que ilustrem como a funcionalidade é utilizada e o valor que ela entrega.
        * Se houver sub-funcionalidades ou opções importantes, detalhe-as.
    * Se o `{{project_link}}` (link do projeto) demonstra funcionalidades específicas, crie referências cruzadas.

10. **🛠️ Tech Stack Detalhado:**
    * Apresente o stack tecnológico completo em uma tabela Markdown bem formatada.
    * Colunas sugeridas: `Categoria` (ex: Backend, Frontend, Banco de Dados, DevOps, IA), `Tecnologia`, `Versão Específica (se aplicável)`, `Propósito no Projeto` (como ela é usada), `Justificativa da Escolha` (por que essa tecnologia foi selecionada, seus benefícios e trade-offs).
    * Seja exaustivo, listando todas as linguagens, frameworks, bibliotecas significativas, bancos de dados, ferramentas de build, plataformas de nuvem, etc.

11. **📂 Estrutura Detalhada do Código-Fonte:**
    * Explique a organização lógica das pastas e arquivos mais críticos do projeto. Qual é a filosofia por trás da estrutura?
    * Detalhe os namespaces, módulos ou pacotes principais e suas responsabilidades e interações.
    * **Inclua uma representação em árvore (ASCII ou similar)** dos diretórios e arquivos chave, seguida de explicações para cada entrada principal. Exemplo:
        \`\`\`
        projeto-raiz/
        ├── src/                # Contém todo o código fonte da aplicação principal.
        │   ├── __init__.py     # Inicializador do pacote src.
        │   ├── main.py         # Ponto de entrada da aplicação ou script principal.
        │   ├── core/           # Lógica de negócio central, modelos de dados.
        │   ├── api/            # Endpoints da API, controladores.
        │   └── utils/          # Funções utilitárias compartilhadas.
        ├── tests/              # Suíte de testes automatizados.
        │   ├── unit/           # Testes unitários.
        │   └── integration/    # Testes de integração.
        ├── docs/               # Documentação adicional, arquivos de design.
        ├── scripts/            # Scripts auxiliares (ex: deploy, migração).
        ├── .env.example        # Exemplo de arquivo de configuração de ambiente.
        ├── requirements.txt    # Dependências do Python.
        ├── Dockerfile          # Configuração para containerização com Docker.
        ├── LICENSE             # Arquivo de licença do projeto.
        └── README.md           # Este arquivo.
        \`\`\`
    * Adapte a árvore e as descrições para refletir o projeto analisado.

12. **📋 Pré-requisitos Avançados:**
    * Liste exaustivamente todas as dependências de software, ferramentas de desenvolvimento, SDKs, versões específicas de linguagens/compiladores e quaisquer configurações de sistema ou variáveis de ambiente que são absolutamente necessárias para instalar, compilar (se aplicável) e executar o projeto corretamente.
    * Especifique versões mínimas e, se relevante, versões testadas.

13. **🚀 Guia de Instalação e Configuração Avançada:**
    * Forneça um guia passo a passo detalhado e inequívoco para que outros desenvolvedores possam clonar, configurar e executar o projeto em seus ambientes.
    * Inclua:
        * Comando para clonar o repositório (usando `git clone {{repo_link}}` ou placeholder).
        * Instruções para configurar diferentes ambientes (desenvolvimento, teste, produção), se houver distinções.
        * Passos para instalar todas as dependências (ex: `pip install -r requirements.txt`, `npm install`).
        * Como criar e configurar arquivos de ambiente (ex: copiar `.env.example` para `.env` e preencher as variáveis). Detalhe cada variável de ambiente necessária e opcional.
        * Comandos exatos para compilar o projeto (se necessário) e para iniciar a aplicação ou seus principais serviços.
        * Instruções detalhadas para Docker / Docker Compose, se o projeto utilizar containerização (como construir a imagem, iniciar containers, volumes, portas).

14. **⚙️ Uso Avançado e Exemplos:**
    * Demonstre exemplos de uso mais complexos, avançados ou menos óbvios do projeto.
    * Inclua exemplos de código, scripts úteis, configurações de interface de linha de comando (CLI) com diferentes opções, ou exemplos de chamadas de API (se for uma API) mostrando diferentes cenários e payloads.
    * Se o `{{project_link}}` é uma ferramenta ou demo interativa, forneça um breve tutorial sobre como interagir com ela para explorar suas capacidades avançadas.

15. **🔧 API Reference (se aplicável):**
    * Se o projeto expõe uma API, forneça uma referência detalhada.
    * Para cada endpoint principal:
        * Método HTTP (GET, POST, PUT, DELETE, etc.).
        * URL completa.
        * Descrição do propósito do endpoint.
        * Parâmetros esperados (de path, query, header, body) com tipos e se são obrigatórios.
        * Exemplo de request body (JSON, XML, etc.).
        * Formatos e exemplos de responses de sucesso e erro (com códigos de status).
    * Sugira um link para uma documentação interativa (Swagger/OpenAPI) se existir ou for planejada. Se não houver API, indique claramente.

16. **🧪 Estratégia de Testes e Qualidade de Código:**
    * Descreva a filosofia e estratégia de testes do projeto.
    * Detalhe os tipos de testes implementados (ex: unitários, de integração, de componentes, end-to-end, de performance, de segurança).
    * Liste as ferramentas, frameworks e bibliotecas de teste utilizados (ex: pytest, JUnit, Selenium, Jest, Mocha).
    * Explique como executar a suíte de testes completa e como gerar relatórios de cobertura de código.
    * Descreva quaisquer políticas de CI/CD (Integração Contínua/Entrega Contínua) e como elas são usadas para manter a qualidade e automatizar o processo de teste e build.

17. **🚢 Deployment Detalhado e Escalabilidade:**
    * Descreva os processos e opções de implantação do projeto em ambientes de produção.
    * Detalhe plataformas específicas (ex: Vercel, AWS EC2/ECS/Lambda, Kubernetes, Google Cloud Run/App Engine, Heroku, Azure App Service).
    * Se `{{project_link}}` for um deploy, explique brevemente a plataforma e o processo de deploy.
    * Discuta considerações sobre escalabilidade (horizontal/vertical), balanceamento de carga, monitoramento de performance, estratégias de logging centralizado e sistemas de alerting.

18. **🤝 Contribuição (Nível Avançado):**
    * Forneça um guia detalhado e acolhedor para potenciais contribuidores:
        * Como fazer fork e clone do repositório.
        * Modelo de branching utilizado (ex: GitFlow, GitHub Flow) e como nomear branches.
        * Convenções de Commit (ex: Conventional Commits - `<tipo>[escopo opcional]: <descrição>`).
        * Guia de Estilo de Código (com link para linters ou formatadores usados, ex: Black, Prettier, ESLint).
        * Processo de Code Review: o que esperar, como preparar um Pull Request para revisão.
    * Instruções sobre como configurar o ambiente de desenvolvimento para facilitar a contribuição e depuração avançada.
    * Use o `{{repo_link}}` para links diretos para a página de Issues (para reportar bugs ou sugerir features) e Pull Requests.
    * Incentive explicitamente as contribuições e explique como a comunidade pode se envolver.

19. **📜 Licença e Aspectos Legais:**
    * Indique claramente a licença sob a qual o projeto é distribuído (ex: MIT, Apache 2.0, GPLv3).
    * Inclua um link para o texto completo do arquivo de licença no repositório (ex: `LICENSE.md` ou `LICENSE`).
    * Se necessário, discuta brevemente as implicações da licença escolhida para usuários e contribuidores.

20. **📚 Publicações, Artigos e Citações (se aplicável):**
    * Se o projeto é de natureza acadêmica, resultou em publicações científicas (artigos, papers, teses), ou se há trabalhos relevantes que devem ser citados como base ou referência, liste-os aqui com links, se possível. Se não aplicável, omita.

21. **👥 Equipe Principal e Colaboradores Chave:**
    * Reconheça formalmente os principais mantenedores, autores e colaboradores que tiveram um papel significativo no desenvolvimento do projeto.
    * Inclua nomes e, se disponível e apropriado, links para seus perfis profissionais (ex: GitHub, LinkedIn - utilizando `{{linkedin_link}}` se fornecido pelo usuário e relevante para o autor do projeto sendo documentado).

22. **🗺️ Roadmap Detalhado e Visão de Longo Prazo:**
    * Apresente as metas de desenvolvimento futuras para o projeto, divididas em curto, médio e longo prazo.
    * Detalhe funcionalidades planejadas, melhorias arquiteturais, ou expansões de escopo.
    * Discuta desafios técnicos ou de produto que se antecipam e possíveis áreas de pesquisa ou inovação futura.

23. **❓ FAQ (Perguntas Frequentes):**
    * Antecipe e responda a perguntas comuns que os usuários, desenvolvedores ou potenciais contribuidores possam ter sobre o projeto.
    * Cubra aspectos como: problemas comuns de instalação, dicas de uso, esclarecimentos sobre funcionalidades, como obter ajuda, etc.

24. **📞 Contato e Suporte:**
    * Indique os canais preferenciais e oficiais para os usuários e desenvolvedores obterem suporte, fazerem perguntas, relatarem problemas ou discutirem o projeto.
    * Pode incluir: link para a seção de Issues do GitHub (`{{repo_link}}/issues`), email de contato específico do projeto, fórum de discussão da comunidade, servidor Discord/Slack, etc.

**Estilo:**
* Formal, preciso, acadêmico (quando o projeto tiver essa natureza), mas sempre didático e acessível.
* Use linguagem clara e objetiva, evitando jargões desnecessários ou explicando-os quando inevitáveis.
* Estruture o conteúdo com parágrafos bem definidos, listas (bullet points ou numeradas), tabelas e blocos de código bem formatados para máxima clareza e legibilidade.
* Incentive ativamente e indique locais apropriados para a inclusão de diagramas (preferencialmente usando Mermaid.js para renderização no GitHub, ou arte ASCII) para ilustrar conceitos complexos como arquitetura, fluxos de dados, etc.
* Emojis podem ser usados com moderação e propósito (ex: `✨ Feature`, `🛠️ Tech Stack`, `🚀 Deploy`) para destacar seções ou conceitos chave, melhorando a escaneabilidade e o apelo visual do README.
"""
