# Stage 1: build Vue frontend
FROM node:22-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci
COPY frontend/ ./
RUN npm run build-only

# Stage 2: Python backend + serve frontend
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY --from=frontend /app/frontend/dist ./frontend/dist

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH" \
    APP_ROOT=/app
EXPOSE 8000

# database.db will be in /app; mount a volume for persistence
CMD ["uvicorn", "summoner_war_webapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
