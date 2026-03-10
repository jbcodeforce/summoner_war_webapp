from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Faction(SQLModel, table=True):
    __tablename__ = "faction"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    summoner_name: str
    owned: bool = False


class Game(SQLModel, table=True):
    __tablename__ = "game"
    id: Optional[int] = Field(default=None, primary_key=True)
    faction_a_id: int = Field(foreign_key="faction.id")
    faction_b_id: int = Field(foreign_key="faction.id")
    winner: str  # "a" or "b"
    played_at: datetime = Field(default_factory=_utc_now)
    player_a_name: Optional[str] = None
    player_b_name: Optional[str] = None
