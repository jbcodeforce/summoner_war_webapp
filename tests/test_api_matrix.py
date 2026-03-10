import pytest


@pytest.fixture
def three_factions(client):
    a = client.post(
        "/api/factions",
        json={"name": "A", "summoner_name": "SA", "owned": True},
    ).json()
    b = client.post(
        "/api/factions",
        json={"name": "B", "summoner_name": "SB", "owned": True},
    ).json()
    c = client.post(
        "/api/factions",
        json={"name": "C", "summoner_name": "SC", "owned": False},
    ).json()
    return a["id"], b["id"], c["id"]


def test_matrix_empty(client):
    r = client.get("/api/matrix")
    assert r.status_code == 200
    assert r.json() == []


def test_matrix_one_pair(client, three_factions):
    fa_id, fb_id, fc_id = three_factions
    # A vs B: two games, A wins both
    client.post(
        "/api/games",
        json={"faction_a_id": fa_id, "faction_b_id": fb_id, "winner": "a"},
    )
    client.post(
        "/api/games",
        json={"faction_a_id": fa_id, "faction_b_id": fb_id, "winner": "a"},
    )
    r = client.get("/api/matrix")
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 1
    assert rows[0]["faction_a_name"] == "A"
    assert rows[0]["faction_b_name"] == "B"
    assert rows[0]["wins_a"] == 2
    assert rows[0]["wins_b"] == 0
    assert rows[0]["total_games"] == 2


def test_matrix_owned_only(client, three_factions):
    fa_id, fb_id, fc_id = three_factions
    client.post(
        "/api/games",
        json={"faction_a_id": fa_id, "faction_b_id": fc_id, "winner": "a"},
    )
    r_all = client.get("/api/matrix")
    r_owned = client.get("/api/matrix?owned_only=true")
    assert len(r_all.json()) == 1
    # C is not owned, so owned_only excludes A vs C
    assert len(r_owned.json()) == 0
