#!/usr/bin/env python3
"""
Seed the database with demo factions and games for Summoner Wars.
Run from project root: uv run python scripts/demo.py
Then start the server: uv run uvicorn summoner_war_webapp.main:app --reload
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from sqlmodel import Session, create_engine, SQLModel, select

# Use same DB path as the app (database.db in project root, or data/database.db when APP_ROOT is set)
_default_root = ROOT
_app_root = Path(os.environ["APP_ROOT"]) if os.environ.get("APP_ROOT") else _default_root
_db_dir = _app_root / "data" if os.environ.get("APP_ROOT") else _app_root
_db_dir.mkdir(parents=True, exist_ok=True)
sqlite_url = f"sqlite:///{_db_dir / 'database.db'}"

# Import after path is set so database module uses correct ROOT if needed
from summoner_war_webapp.models import Faction, Game
from datetime import datetime, timezone

def main():
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Check if already seeded
        existing = session.exec(select(Faction)).first()
        if existing is not None:
            print("Database already has data. Skipping seed.")
            return

        factions = [
            Faction(name="Phoenix Elves", summoner_name="Maelorn", owned=True),
            Faction(name="Cave Goblins", summoner_name="Screetch", owned=True),
            Faction(name="Tundra Orcs", summoner_name="Grognack", owned=True),
            Faction(name="Vanguard", summoner_name="Rime", owned=False),
        ]
        for f in factions:
            session.add(f)
        session.commit()
        session.refresh(factions[0])
        session.refresh(factions[1])
        fa, fb = factions[0].id, factions[1].id

        games = [
            Game(faction_a_id=fa, faction_b_id=fb, winner="a", played_at=datetime.now(timezone.utc), player_a_name="Alice", player_b_name="Bob"),
            Game(faction_a_id=fa, faction_b_id=fb, winner="b", played_at=datetime.now(timezone.utc)),
            Game(faction_a_id=fa, faction_b_id=fb, winner="a", played_at=datetime.now(timezone.utc)),
        ]
        for g in games:
            session.add(g)
        session.commit()

    print("Demo data seeded. Start the server with:")
    print("  uv run uvicorn summoner_war_webapp.main:app --reload")
    print("Then open http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
