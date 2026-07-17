FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.14-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY . .

ENV PATH="/opt/venv/bin:$PATH"

# Playwright browser + OS deps (needed by the scraping worker)
RUN playwright install --with-deps firefox

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]