import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from sw_backend.database import create_db_and_tables
from sw_backend.logging_config import setup_logging
from sw_backend.routers import factions, games, matrix

setup_logging()
log = logging.getLogger("summoner_wars_webapp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up: creating DB and tables")
    create_db_and_tables()
    yield
    log.info("Shutting down")


app = FastAPI(title="Summoner Wars Tracker", lifespan=lifespan)


@app.middleware("http")
async def log_requests(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    log.info(
        "%s %s -> %s %.1fms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


# API routes under /api
app.include_router(factions.router, prefix="/api")
app.include_router(games.router, prefix="/api")
app.include_router(matrix.router, prefix="/api")

# Resolve path to frontend dist (when built)
from sw_backend.database import ROOT
DIST_DIR = ROOT / "frontend" / "dist"


@app.exception_handler(Exception)
def log_unhandled_exception(request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    log.exception("Unhandled exception: %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


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
