# Summoner Wars Game tracking app

This is a simple web app in Python to track [Summoner Wars](https://www.plaidhatgames.com/board-games/summoner-wars/) games.

## Features

- [x] use uv to manage the python app, dependencies
- [x] Backend with FastAPI serving a Vue.js app (frontend dist delivered from the same server)
- [x] Backend with games persisted in SQLite
- [x] Data models: **Faction** (name, summoner_name, owned). **Game**: two factions, winner, date, optional player names
- [x] UI: enter new games, table of all games with edit/delete
- [x] UI: faction vs faction matrix table
- [x] Factions owned: backend stores `owned` per faction; matrix can filter by owned factions only
- [x] Dockerized application
- [x] TDD: pytest tests for the backend API
- [x] Script to run in demo mode

## Setup

### Backend (Python)

- **uv** is used for dependencies. Install [uv](https://docs.astral.sh/uv/) if needed.
- From the project root:
  - `uv sync` — install dependencies
  - `uv run uvicorn summoner_war_webapp.main:app --port 9001 --reload` — run the API (and serve the frontend when built)

### Frontend (Vue 3 + Vite)

- From `frontend/`:
  - `npm install`
  - `npm run dev` — development server (proxy to backend if needed)
  - `npm run build-only` — build for production (output in `frontend/dist/`)

To serve the app from the backend, build the frontend once, then run the backend from the project root. The backend serves `frontend/dist` at `/` and the API under `/api`.

## Demo mode

1. Seed demo data:  
   `uv run python scripts/demo.py`
2. Start the server:  
   `uv run uvicorn summoner_war_webapp.main:app --reload`
3. Open http://127.0.0.1:8000

The demo seeds a few factions and games. Re-running the script skips seeding if data already exists.

## Docker

- Build and run with Docker Compose:  
  `docker compose up --build`  
  App is at http://localhost:8000. Data is stored in a volume (`summoner_data` → `/app/data`).

- Or build the image and run the container manually, setting `APP_ROOT=/app` and mounting a volume for `/app/data` if you want persistence.

## Tests

- Run backend API tests:  
  `uv run pytest tests/`

## API overview

- **Factions**: `GET/POST /api/factions`, `GET/PUT/DELETE /api/factions/{id}` (optional `?owned=true|false` on list)
- **Games**: `GET/POST /api/games`, `GET/PUT/DELETE /api/games/{id}` (optional `?faction_id=` on list)
- **Matrix**: `GET /api/matrix?owned_only=true|false` — faction vs faction win counts
