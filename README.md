# Bot de Concurso

Um sistema moderno e inteligente para buscar, acompanhar e organizar editais de concursos públicos.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Sobre o Projeto

O **Bot de Concurso** foi desenvolvido para simplificar a vida de quem estuda para concursos públicos. O sistema realiza a coleta automatizada (scraping) de dados de diversos portais, padroniza as informações, baixa os PDFs dos editais e os disponibiliza através de uma API rápida.

## Principais Funcionalidades

- **Extração Automatizada (Scraping):** Coleta de editais ativos de concursos, capturando dados como órgão, cargo, nível de escolaridade, salário e data limite.
- **Pipeline Paralelo:** Arquitetura producer/consumer com `asyncio.Queue` — o scraping dos dados e o processamento dos PDFs rodam de forma concorrente, sem bloqueios.
- **Download e Armazenamento de Editais (PDFs):** Para cada concurso encontrado, o sistema navega até a página do edital, coleta os links dos PDFs e faz o upload automaticamente para armazenamento em nuvem S3.
- **Integração com S3:** Upload dos arquivos para qualquer provedor compatível com o protocolo S3 (AWS S3, Cloudflare R2, MinIO, etc.), com URL pública retornada junto aos dados de cada concurso.
- **Armazenamento Otimizado:** Uso de Redis para armazenamento de alta performance dos dados extraídos.
- **Automação de Tarefas (Workers):** Scraping executado como jobs independentes e também através de GitHub Actions de forma agendada.

## Estrutura e Arquitetura

O projeto é estruturado focado no Backend e automação:

```text
bot_concurso/
├── app/                      # Backend (Python / FastAPI)
│   ├── main.py               # Ponto de entrada da API
│   ├── infra/                # Comunicação com serviços externos (Redis, S3)
│   │   ├── redis_client.py   # Persistência dos dados de concursos
│   │   └── s3_client.py      # Upload de PDFs para armazenamento em nuvem
│   ├── modules/              # Lógica profunda de negócio
│   │   ├── config/           # Configurações e variáveis de ambiente
│   │   ├── scraping/         # Scripts e algoritmos de extração + download de PDFs
│   │   └── workers/          # Pipeline producer/consumer para processamento paralelo
│   └── routes/               # Rotas da API
│
├── .github/workflows/        # Automação CI/CD (Scraping agendado)
├── docker-compose.yaml       # Configuração de serviços via Docker (Redis)
├── Makefile                  # Comandos facilitadores
└── requirements.txt          # Especificações de dependências do Python
```

## Como Executar Localmente

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

### Passo 3: Configurando as variáveis de ambiente

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

| Variável | Descrição | Obrigatória |
| --- | --- | --- |
| `REDIS_URL` | URL de conexão com o Redis | Sim |
| `S3_ENDPOINT` | Endpoint do provedor S3 (ex.: `https://s3.amazonaws.com`) | Sim |
| `S3_REGION` | Região do bucket (padrão: `us-west-1`) | Não |
| `S3_ACCESS_KEY` | Chave de acesso S3 | Sim |
| `S3_SECRET_KEY` | Chave secreta S3 | Sim |
| `S3_BUCKET` | Nome do bucket (padrão: `editais-bot-concurso`) | Não |

### Passo 4: Executando o Scraping

Para realizar a extração inicial dos dados usando o worker:

```bash
make run-scraping
```

O worker irá:

1. **Coletar** todos os editais ativos do portal de concursos
2. **Em paralelo**, para cada concurso, navegar até a página do edital e baixar os PDFs encontrados
3. **Fazer upload** de cada PDF para o S3 e salvar a URL pública junto ao registro do concurso no Redis

### Passo 5: Inicializando a API (FastAPI)

```bash
make run
```

Após as mensagens de sucesso, a API estará ativa em `http://localhost:8000`. A documentação interativa (Swagger) estará disponível em `http://localhost:8000/docs`.

## Scraping Automático (GitHub Actions)

O repositório possui um workflow do GitHub Actions configurado (`fetch_contests.yaml`) que roda todos os dias às 11:00 UTC (08:00 no horário de Brasília) para manter os dados no banco atualizados automaticamente. Ele requer os seguintes **Secrets** configurados no repositório:

| Secret | Descrição |
| --- | --- |
| `REDIS_URL` | URL de conexão com o Redis na nuvem |
| `S3_ENDPOINT` | Endpoint do provedor S3 |
| `S3_REGION` | Região do bucket S3 |
| `S3_ACCESS_KEY` | Chave de acesso S3 |
| `S3_SECRET_KEY` | Chave secreta S3 |
