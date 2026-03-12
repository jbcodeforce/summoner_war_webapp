from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from summoner_war_webapp.database import get_session
from summoner_war_webapp.models import Faction, Game
from summoner_war_webapp.schemas import MatrixEntry

router = APIRouter(prefix="/matrix", tags=["matrix"])


@router.get("", response_model=list[MatrixEntry])
def get_matrix(
    owned_only: bool = Query(False),
    session: Session = Depends(get_session),
):
    factions_stmt = select(Faction)
    if owned_only:
        factions_stmt = factions_stmt.where(Faction.owned == True)
    factions = {f.id: f for f in session.exec(factions_stmt)}
    faction_ids = set(factions.keys())

    games = session.exec(select(Game)).all()
    # Pair (min_id, max_id) -> (wins_a, wins_b) where a = first faction, b = second
    pair_wins: dict[tuple[int, int], tuple[int, int]] = {}

    for g in games:
        if g.faction_a_id not in faction_ids or g.faction_b_id not in faction_ids:
            continue
        key = (min(g.faction_a_id, g.faction_b_id), max(g.faction_a_id, g.faction_b_id))
        if key not in pair_wins:
            pair_wins[key] = (0, 0)
        w_a, w_b = pair_wins[key]
        if g.faction_a_id < g.faction_b_id:
            if g.winner == "a":
                pair_wins[key] = (w_a + 1, w_b)
            else:
                pair_wins[key] = (w_a, w_b + 1)
        else:
            if g.winner == "b":
                pair_wins[key] = (w_a + 1, w_b)
            else:
                pair_wins[key] = (w_a, w_b + 1)

    result = []
    for (id_a, id_b), (wins_a, wins_b) in pair_wins.items():
        fa, fb = factions[id_a], factions[id_b]
        result.append(
            MatrixEntry(
                faction_a_id=id_a,
                faction_a_name=fa.name,
                faction_b_id=id_b,
                faction_b_name=fb.name,
                wins_a=wins_a,
                wins_b=wins_b,
                total_games=wins_a + wins_b,
            )
        )
    return result
