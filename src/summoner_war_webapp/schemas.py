from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Faction
class FactionCreate(BaseModel):
    name: str
    summoner_name: str
    owned: bool = False


class FactionUpdate(BaseModel):
    name: Optional[str] = None
    summoner_name: Optional[str] = None
    owned: Optional[bool] = None


class FactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    summoner_name: str
    owned: bool


# Game
class GameCreate(BaseModel):
    faction_a_id: int
    faction_b_id: int
    winner: str  # "a" or "b"
    played_at: Optional[datetime] = None
    player_a_name: Optional[str] = None
    player_b_name: Optional[str] = None


class GameUpdate(BaseModel):
    faction_a_id: Optional[int] = None
    faction_b_id: Optional[int] = None
    winner: Optional[str] = None
    played_at: Optional[datetime] = None
    player_a_name: Optional[str] = None
    player_b_name: Optional[str] = None


class GameRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    faction_a_id: int
    faction_b_id: int
    winner: str
    played_at: datetime
    player_a_name: Optional[str] = None
    player_b_name: Optional[str] = None


# Matrix
class MatrixEntry(BaseModel):
    faction_a_id: int
    faction_a_name: str
    faction_b_id: int
    faction_b_name: str
    wins_a: int
    wins_b: int
    total_games: int
