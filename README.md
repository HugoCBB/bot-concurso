<div align="center">
  <h1>🤖 Bot de Concurso</h1>
  <p>Um sistema moderno e inteligente para buscar, acompanhar e organizar editais de concursos públicos.</p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright" />
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  </p>
</div>

<br />

## 📖 Sobre o Projeto

O **Bot de Concurso** foi desenvolvido para simplificar a vida de quem estuda para concursos públicos. O sistema realiza a coleta automatizada (scraping) de dados de diversos portais, padroniza as informações e as disponibiliza através de uma API rápida. 

## ✨ Principais Funcionalidades

- **🕷️ Extração Automatizada (Scraping):** Coleta de editais ativos de concursos, capturando dados corporativos como o órgão, cargo, nível de escolaridade, salário e data limite.
- **⚡ API Performática:** Backend construído com FastAPI para servir os dados da forma mais rápida e escalável possível.
- **💾 Armazenamento Otimizado:** Uso de Redis para armazenamento de alta performance dos dados extraídos.
- **⚙️ Automação de Tarefas (Workers):** Scraping executado como jobs independentes e também através de GitHub Actions de forma agendada.

## 🏗️ Estrutura e Arquitetura

O projeto é estruturado focado no Backend e automação:

```text
bot_concurso/
├── app/                      # 🗄️ Backend (Python / FastAPI)
│   ├── main.py               # Ponto de entrada da API
│   ├── infra/                # Comunicação com serviços externos (Redis)
│   ├── modules/              # Lógica profunda de negócio
│   │   ├── scraping/         # Scripts e algoritmos de extração
│   │   └── workers/          # Scripts que serão executadas em segundo plano (jobs)
│   └── routes/               # Rotas da API
│
├── .github/workflows/        # ⚙️ Automação CI/CD (Scraping agendado)
├── docker-compose.yaml       # 🐋 Configuração de serviços via Docker (Redis)
├── Makefile                  # 🛠️ Comandos facilitadores
└── requirements.txt          # 📦 Especificações de dependências do Python
```

## 🚀 Como Executar Localmente

### Pré-requisitos e Dependências
Para iniciar a aplicação localmente, certifique-se de ter instalado no seu computador:
- **Python 3.10+**
- **Docker** e **Docker Compose** (para o Redis)
- **Make**

### Passo 1: Inicializando o Banco de Dados (Redis)

O projeto usa Redis para armazenar os concursos. Levante o contêiner usando Docker:

```bash
docker compose up -d
```

### Passo 2: Configurando o ambiente Python

Abra seu terminal favorito, acesse o repositório clonado e inicie seu ambiente isolado:

```bash
# 1. Crie e ative um ambiente virtual isolado p/ manter os módulos organizados
python3 -m venv venv
source venv/bin/activate  # NO WINDOWS, UTILIZE: venv\Scripts\activate

# 2. Instale os requerimentos globais da aplicação Python e as dependências do Playwright
pip install -r requirements.txt
playwright install firefox
```

### Passo 3: Executando o Scraping (Opcional, os dados precisam existir no Redis)

Para realizar a extração inicial dos dados usando o worker:

```bash
make run-scraping
```

### Passo 4: Inicializando a API (FastAPI)

```bash
# Levante o servidor de desenvolvimento
make run
```
> Após as mensagens de sucesso aparecerem, sua API já estará ativa em: `http://localhost:8000`. Se desejar, explore a documentação em conjunto via visualização interativa no Swagger acessando `http://localhost:8000/docs`.

## 🤖 Scraping Automático (GitHub Actions)
O repositório possui um workflow do GitHub Actions configurado (`fetch_contests.yaml`) que roda todos os dias às 11:00 UTC (08:00 no horário de Brasília) para manter os dados no banco atualizados automaticamente. Ele requer que haja uma `REDIS_URL` configurada nos **Secrets** do repositório para conectar ao seu banco de dados na nuvem.

