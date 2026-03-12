"""
Configure application logging to a logs/ folder and console.
Uses APP_ROOT when set (e.g. in Docker), otherwise project root.
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_default_root = Path(__file__).resolve().parent.parent.parent
ROOT = Path(os.environ["APP_ROOT"]) if os.environ.get("APP_ROOT") else _default_root
LOGS_DIR = ROOT / "logs"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()


def setup_logging() -> None:
    """Create logs directory, add file and console handlers to the root logger."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "app.log"

    root = logging.getLogger()
    root.setLevel(LOG_LEVEL)
    # Avoid duplicate handlers when reloading
    for h in root.handlers[:]:
        root.removeHandler(h)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(fmt)
    root.addHandler(console_handler)

    log = logging.getLogger("summoner_war_webapp")
    log.info("Logging to %s (level=%s)", log_file, LOG_LEVEL)
