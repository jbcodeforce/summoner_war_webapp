from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from summoner_war_webapp.database import get_session
from summoner_war_webapp.models import Faction
from summoner_war_webapp.schemas import FactionCreate, FactionRead, FactionUpdate

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("", response_model=list[FactionRead])
def list_factions(
    owned: bool | None = Query(None),
    session: Session = Depends(get_session),
):
    stmt = select(Faction)
    if owned is not None:
        stmt = stmt.where(Faction.owned == owned)
    return list(session.exec(stmt))


@router.post("", response_model=FactionRead)
def create_faction(faction: FactionCreate, session: Session = Depends(get_session)):
    db_faction = Faction.model_validate(faction)
    session.add(db_faction)
    session.commit()
    session.refresh(db_faction)
    return db_faction


@router.get("/{faction_id}", response_model=FactionRead)
def get_faction(faction_id: int, session: Session = Depends(get_session)):
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")
    return faction


@router.put("/{faction_id}", response_model=FactionRead)
def update_faction(
    faction_id: int, payload: FactionUpdate, session: Session = Depends(get_session)
):
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(faction, k, v)
    session.add(faction)
    session.commit()
    session.refresh(faction)
    return faction


@router.delete("/{faction_id}", status_code=204)
def delete_faction(faction_id: int, session: Session = Depends(get_session)):
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")
    session.delete(faction)
    session.commit()
