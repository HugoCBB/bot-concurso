<div align="center">
  <h1>🤖 Bot de Concurso</h1>
  <p>Um sistema moderno e inteligente para buscar, acompanhar e organizar editais de concursos públicos.</p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  </p>
</div>

<br />

## � Sobre o Projeto

O **Bot de Concurso** foi desenvolvido para simplificar a vida de quem estuda para concursos públicos. O sistema realiza a coleta automatizada (scraping) de dados de diversos portais, padroniza as informações e as disponibiliza através de uma API rápida. O frontend apresenta esses dados de forma organizada através de uma interface limpa, vibrante e focada na experiência do usuário.

## ✨ Principais Funcionalidades

- **🕷️ Extração Automatizada (Scraping):** Coleta de editais ativos de concursos, capturando dados corporativos como o órgão, cargo, nível de escolaridade, salário e data limite.
- **⚡ API Performática:** Backend construído com FastAPI para servir os dados da forma mais rápida e escalável possível.
- **📱 Interface Moderna e Responsiva:** Frontend inteiramente desenvolvido em React com Tailwind CSS e Shadcn UI, garantindo facilidade de uso em qualquer tamanho de tela e acesso a modos claro e escuro.
- **📑 Paginação Dinâmica:** Navegação simples e rápida pelas diversas páginas do catálogo de vagas e editais.
- **🏷️ Identificação Inteligente:** Classificação visual automática de vagas por estado (SP, RJ, MG) e fácil redirecionamento para o edital oficial.

## 🏗️ Estrutura e Arquitetura

O projeto adota uma arquitetura web moderna e completamente desacoplada:

```text
bot_concurso/
├── app/                      # 🗄️ Backend (Python / FastAPI)
│   ├── main.py               # Ponto de entrada da API, roteamento e paginação
│   ├── modules/              # Lógica profunda de negócio
│   │   ├── scraping/         # Scripts e algoritmos de extração
│   │   └── utils/            # Utilitários de manipulação de disco
│   └── datas/                # Armazenamento local dos dados em JSON
│   └── workes/              # Scripts que serao executadas em segundo plano
│
├── frontend/                 # 💻 Frontend (React / Vite)
│   ├── src/
│   │   ├── components/ui/    # Componentes estilizados exportados do Shadcn UI
│   │   ├── services/         # Configurações do cliente Axios (Consumo da API local)
│   │   ├── App.tsx           # Aplicação principal, gerenciamento de estado e Grid Render
│   │   └── index.css         # Variáveis e temas (Tailwind/Oklch) para cores dinâmicas
│   ├── package.json          # Metadados e dependências Node configuradas
│   └── vite.config.ts        # Opções do bundler Vite
│
└── requirements.txt          # 📦 Especificações de dependências do Python
```

## � Como Executar Localmente

### Pré-requisitos e Dependências
Para iniciar a aplicação localmente, certifique-se de ter instalado no seu computador:
- **Python 3.10+**
- **Node.js 18+** e o gerenciador de pacotes **npm**

### Passo 1: Inicializando o Backend (FastAPI)

Abra seu terminal favorito, acesse o repositório clonado e inicie seu ambiente isolado:

```bash
# 1. Entre no diretório do Backend
cd app

# 2. Crie e ative um ambiente virtual isolado p/ manter os módulos organizados
python3 -m venv venv
source venv/bin/activate  # NO WINDOWS, UTILIZE: venv\Scripts\activate

# 3. Instale os requerimentos globais da aplicação Python
pip install -r ../requirements.txt

# 4. Levante o backend com reload ativado!
uvicorn main:app --reload --port 8000
```
> Após as mensagens de sucesso aparecerem, sua API já estará ativa em: `http://localhost:8000`. Se desejar, explore a documentação em conjunto via visualização interativa no Swagger acessando `http://localhost:8000/docs`.

### Passo 2: Inicializando o Frontend (React)

Com o processo do Backend minimizado e executando livremente, abra um **novo terminal** na pasta raiz e siga os passos:

```bash
# 1. Entre no diretório do Frontend Web
cd frontend

# 2. Faça o download e instale todas as dependências JavaScript/React
npm install

# 3. Inicie o Vite em modo de desenvolvimento local
npm run dev
```
> O sistema irá fornecer um link rápido em verde no terminal, tipicamente apontando para `http://localhost:5173/`. Cole essa URL no seu navegador e aproveite o projeto!

