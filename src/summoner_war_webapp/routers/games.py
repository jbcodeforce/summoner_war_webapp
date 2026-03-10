from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from summoner_war_webapp.database import get_session
from summoner_war_webapp.models import Game
from summoner_war_webapp.schemas import GameCreate, GameRead, GameUpdate

router = APIRouter(prefix="/games", tags=["games"])


@router.get("", response_model=list[GameRead])
def list_games(
    faction_id: int | None = Query(None),
    session: Session = Depends(get_session),
):
    stmt = select(Game)
    if faction_id is not None:
        stmt = stmt.where((Game.faction_a_id == faction_id) | (Game.faction_b_id == faction_id))
    stmt = stmt.order_by(Game.played_at.desc())
    return list(session.exec(stmt))


@router.post("", response_model=GameRead)
def create_game(game: GameCreate, session: Session = Depends(get_session)):
    data = game.model_dump()
    if data.get("played_at") is None:
        from datetime import datetime, timezone
        data["played_at"] = datetime.now(timezone.utc)
    db_game = Game.model_validate(data)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: int, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.put("/{game_id}", response_model=GameRead)
def update_game(
    game_id: int, payload: GameUpdate, session: Session = Depends(get_session)
):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(game, k, v)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@router.delete("/{game_id}", status_code=204)
def delete_game(game_id: int, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    session.delete(game)
    session.commit()
