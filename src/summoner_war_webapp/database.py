import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

_default_root = Path(__file__).resolve().parent.parent.parent
ROOT = Path(os.environ["APP_ROOT"]) if os.environ.get("APP_ROOT") else _default_root
# In Docker (APP_ROOT set) use data subdir for volume mount; otherwise project root
_db_dir = ROOT / "data" if os.environ.get("APP_ROOT") else ROOT
_db_dir.mkdir(parents=True, exist_ok=True)
sqlite_url = f"sqlite:///{_db_dir / 'database.db'}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
