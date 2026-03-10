from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from summoner_war_webapp.database import create_db_and_tables
from summoner_war_webapp.routers import factions, games, matrix


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Summoner Wars Tracker", lifespan=lifespan)

# API routes under /api
app.include_router(factions.router, prefix="/api")
app.include_router(games.router, prefix="/api")
app.include_router(matrix.router, prefix="/api")

# Resolve path to frontend dist (when built)
from summoner_war_webapp.database import ROOT
DIST_DIR = ROOT / "frontend" / "dist"


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve Vue SPA: mount static assets first, then catch-all for index.html
if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        """Serve static file if it exists, else index.html for SPA routes."""
        if full_path.startswith("api"):
            return {"detail": "Not Found"}
        if full_path:
            file_path = DIST_DIR / full_path
            if file_path.is_file():
                return FileResponse(file_path)
        return FileResponse(DIST_DIR / "index.html")
