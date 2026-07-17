# Bot de Concurso

Um sistema moderno e inteligente para buscar, acompanhar e organizar editais de concursos públicos.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Sobre o Projeto

O **Bot de Concurso** foi desenvolvido para simplificar a vida de quem estuda para concursos públicos. O sistema realiza a coleta automatizada (scraping) de dados de portais de concursos, padroniza as informações, baixa os PDFs dos editais e os disponibiliza através de uma API rápida.

O **PostgreSQL** é a fonte de verdade (histórico e deduplicação), o **Redis** funciona como cache quente para a API, e o **S3** guarda os PDFs dos editais.

## Principais Funcionalidades

- **Extração Automatizada (Scraping):** Coleta de editais ativos, capturando órgão, cargo, nível, data limite e link.
- **Pipeline Paralelo:** Arquitetura producer/consumer com `asyncio.Queue` — um pool de workers processa vários concursos ao mesmo tempo, com semáforo limitando as páginas simultâneas do navegador.
- **Isolamento de Falhas:** Um concurso que falha (página inacessível, PDF quebrado) é registrado e ignorado — nunca derruba o job inteiro.
- **Persistência Idempotente:** Cada concurso tem um `fingerprint` (hash de órgão + link + data). O `UPSERT` por fingerprint evita duplicatas, então rodar o scraping várias vezes é seguro.
- **Salvamento Incremental:** Cada concurso é gravado no Postgres assim que é processado — um crash no meio do job não perde o que já foi feito.
- **Limpeza de Armazenamento:** No início de cada job, concursos com data limite vencida são removidos do banco **e** seus PDFs são apagados do S3, mantendo o storage sob controle.
- **Download e Armazenamento de Editais (PDFs):** Para cada concurso, o sistema coleta os links dos PDFs, baixa (com retry/backoff) e faz upload para o S3.
- **Cache com Redis:** A API lê do cache Redis; em cache frio, busca no Postgres e reaquece o cache.
- **Agendamento (Worker arq):** Um worker `arq` executa o scraping via cron (a cada 6h) e aceita disparos sob demanda pela API.
- **Scraping Agendado (GitHub Actions):** Alternativa/adicional ao worker, roda o scraping em um cron diário.

## Estrutura e Arquitetura

```text
bot_concurso/
├── app/                          # Backend (Python / FastAPI)
│   ├── server/
│   │   └── main.py               # Ponto de entrada da API (uvicorn server.main:app)
│   ├── infra/                    # Comunicação com serviços externos
│   │   ├── db.py                 # Engine/sessão async do Postgres (SQLAlchemy)
│   │   ├── redis_client.py       # Cache dos concursos
│   │   ├── s3_client.py          # Upload/remoção de PDFs no S3
│   │   └── arq_client.py         # Conexão/fila do worker arq
│   ├── modules/
│   │   ├── config/               # Configurações e variáveis de ambiente
│   │   ├── models/               # Modelos ORM (Contest, Edital)
│   │   ├── repository/           # Camada de acesso a dados (upsert, cleanup, leitura)
│   │   ├── scraping/             # Extração + transformação + download de PDFs
│   │   └── workers/              # Pipeline (run_scraping), CLI e WorkerSettings do arq
│   ├── routes/                   # Rotas da API
│   ├── migrations/               # Migrações Alembic
│   └── alembic.ini
│
├── .github/workflows/            # Scraping agendado (CI)
├── docker-compose.yaml           # postgres, redis, migrate, api, worker
├── Makefile                      # Comandos facilitadores
└── README.md
```

### Fluxo de um Job de Scraping

```
limpeza de vencidos (DB + S3)  ->  scraping da lista  ->  processa cada concurso
        (cleanup_expired)             (producer)          (workers, em paralelo)
                                                                    |
                                              baixa PDFs -> S3  +  UPSERT incremental (Postgres)
                                                                    |
                                                        refresh do cache Redis (no fim)
```

## Como Executar (Docker — recomendado)

O jeito mais simples de subir tudo (Postgres, Redis, migrações, API e worker):

### Pré-requisitos
- **Docker** e **Docker Compose**
- **Make** (opcional, mas os comandos abaixo o usam)

### Passo 1: Variáveis de ambiente
```bash
cd app && cp .env.example .env    # preencha as credenciais S3 (Postgres/Redis já apontam para o compose)
```

### Passo 2: Subir a stack
```bash
make up        # docker compose up -d --build
```
Isso sobe, na ordem: **postgres** → **migrate** (`alembic upgrade head`, roda uma vez) → **api** + **worker**.

### Passo 3: Rodar um scraping
```bash
make refresh        # enfileira um job no worker (via API POST /api/contests/refresh)
# ou:
make run-scraping   # roda o pipeline uma vez, direto (sem fila)
make logs-worker    # acompanhar os logs do worker
```

A API fica em `http://localhost:8000` e a documentação (Swagger) em `http://localhost:8000/docs`.

### Comandos do Makefile

| Comando | O que faz |
| --- | --- |
| `make up` | Build + sobe todos os serviços |
| `make down` | Para e remove os contêineres |
| `make logs` / `make logs-worker` | Acompanha os logs |
| `make migrate` | Aplica as migrações (`alembic upgrade head`) |
| `make refresh` | Enfileira um job de scraping via API |
| `make run-scraping` | Roda o scraping uma vez (nativo) |
| `make scrape` | Roda o scraping uma vez (contêiner one-off) |
| `make psql` | Abre um shell `psql` no banco |

## Como Executar Localmente (sem Docker)

Requer **Python 3.14**, além de um Postgres e Redis acessíveis.

```bash
# 1. Ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Dependências + navegador
pip install -r app/requirements.txt
playwright install firefox

# 3. Postgres + Redis (via Docker, só a infra)
docker compose up -d postgres redis migrate

# 4. Variáveis de ambiente
cd app && cp .env.example .env

# 5. Rodar o scraping
python -m modules.workers.run_job     # ou: make run-scraping (na raiz)

# 6. Subir a API
fastapi dev server/main.py            # a partir da pasta app/
```

## Variáveis de Ambiente

| Variável | Descrição | Obrigatória |
| --- | --- | --- |
| `DATABASE_URL` | Conexão Postgres (driver async `postgresql+psycopg://...`) | Sim |
| `REDIS_URL` | URL de conexão com o Redis | Sim |
| `S3_ENDPOINT` | Endpoint do provedor S3 | Sim |
| `S3_REGION` | Região do bucket (padrão: `us-west-1`) | Não |
| `S3_ACCESS_KEY` | Chave de acesso S3 | Sim |
| `S3_SECRET_KEY` | Chave secreta S3 | Sim |
| `S3_BUCKET` | Nome do bucket (padrão: `editais-bot-concurso`) | Não |
| `CORS_URL` | Origem permitida no CORS da API | Não |

### Postgres na Supabase (produção / CI)

Use a string do **Session pooler** (IPv4, porta 5432 — funciona no GitHub Actions e mantém os prepared statements do psycopg3/Alembic):

```
postgresql+psycopg://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres?sslmode=require
```

- O usuário é `postgres.<project-ref>` (não apenas `postgres`).
- Mantenha o prefixo `postgresql+psycopg://` e `?sslmode=require`.
- **Não** use o Transaction pooler (porta 6543) para migrações — o modo transaction quebra os prepared statements.
- A senha do banco **não** é a do seu login (GitHub SSO); é definida na criação do projeto e pode ser redefinida em *Project Settings → Database*.

## Migrações (Alembic)

O schema é versionado com Alembic (não use `create_all` em produção).

```bash
cd app
alembic upgrade head                       # aplica todas as migrações
alembic revision --autogenerate -m "msg"   # gera nova migração a partir dos modelos
```

No Docker, o serviço `migrate` roda `alembic upgrade head` automaticamente antes da API/worker subirem.

## API

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/contests/` | Lista paginada de concursos (cache Redis → Postgres) |
| `POST` | `/api/contests/refresh` | Enfileira um job de scraping no worker |
| `GET` | `/` | Health check |

## Scraping Automático (GitHub Actions)

O workflow `fetch_contests.yaml` roda um cron diário (11:00 UTC / 08:00 Brasília): instala as dependências, aplica as migrações (`alembic upgrade head`) e executa o scraper. Requer os **Secrets** no repositório:

| Secret | Descrição |
| --- | --- |
| `DATABASE_URL` | Conexão Postgres (Session pooler da Supabase — IPv4) |
| `REDIS_URL` | URL de conexão com o Redis na nuvem |
| `S3_ENDPOINT` | Endpoint do provedor S3 |
| `S3_REGION` | Região do bucket S3 |
| `S3_ACCESS_KEY` | Chave de acesso S3 |
| `S3_SECRET_KEY` | Chave secreta S3 |
