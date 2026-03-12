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
sqlite_url = f"sqlite:///{_db_dir / 'sw_database.db'}"

# Import after path is set so database module uses correct ROOT if needed
from sw_backend.models import Faction, Game
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
            Faction(name="Jungles Elves", summoner_name="Abua Shi", owned=True),
            Faction(name="Filth", summoner_name="The Demagogue", owned=True),
            Faction(name="Deep Benders", summoner_name="Endrich", owned=True),
            Faction(name="Mercenaries", summoner_name="Farrah Oathbreaker", owned=True),
            Faction(name="Swamp Mercenaries", summoner_name="Glurblub", owned=True),
            Faction(name="Tundra Orcs", summoner_name="Grognack", owned=True),
            Faction(name="Tundra Guild", summoner_name="Hogar", owned=True),
            Faction(name="Fallen Phoenix", summoner_name="Immortal Elien", owned=True),
            Faction(name="Cloaks", summoner_name="Jexik", owned=True),
            Faction(name="Sand Goblins", summoner_name="Krusk", owned=True),
            Faction(name="Fallen Kingdom", summoner_name="Mad Sirian", owned=True),
            Faction(name="Sand Cloaks", summoner_name="Marek", owned=True),
            Faction(name="Jungle Shadows", summoner_name="Melundak", owned=True),
            Faction(name="Vargath Vanguards", summoner_name="Moyra Skylark", owned=True),
            Faction(name="Swamp Orcs", summoner_name="Mugglug", owned=True),
            Faction(name="Jungle Elves", summoner_name="Nikuya Na", owned=True),
            Faction(name="Guild Dwarves", summoner_name="Oldin", owned=True),
            Faction(name="Phoenix Guild", summoner_name="Prince Elien", owned=True),
            Faction(name="Fallen Kingdom", summoner_name="Red-Talus", owned=True),



            Faction(name="Vanguards", summoner_name="Sera Eldwyn", owned=True),

            Faction(name="Shadow Elves", summoner_name="Selundar", owned=True),
            Faction(name="Cave Golblins", summoner_name="Sneeks", owned=True),
            Faction(name="Mountain Vargath", summoner_name="Sunderved", owned=True),
            Faction(name="Renders", summoner_name="Taculu", owned=True),
            Faction(name="Cave Filth", summoner_name="The Warden", owned=True),
            Faction(name="Deep Dwarves", summoner_name="Tundle", owned=True)


        ]
        for f in factions:
            session.add(f)
        session.commit()
        session.refresh(factions[0])
        session.refresh(factions[1])
        fa, fb = factions[0].id, factions[1].id
        """
        games = [
            Game(faction_a_id=fa, faction_b_id=fb, winner="a", played_at=datetime.now(timezone.utc), player_a_name="Alice", player_b_name="Bob"),
            Game(faction_a_id=fa, faction_b_id=fb, winner="b", played_at=datetime.now(timezone.utc)),
            Game(faction_a_id=fa, faction_b_id=fb, winner="a", played_at=datetime.now(timezone.utc)),
        ]
        for g in games:
            session.add(g)
        session.commit()
        """

    print("Demo data seeded. Start the server with:")
    print("  uv run uvicorn summoner_war_webapp.main:app --reload")
    print("Then open http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
