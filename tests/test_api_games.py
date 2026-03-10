import pytest


@pytest.fixture
def two_factions(client):
    a = client.post(
        "/api/factions",
        json={"name": "Faction A", "summoner_name": "Summoner A", "owned": True},
    ).json()
    b = client.post(
        "/api/factions",
        json={"name": "Faction B", "summoner_name": "Summoner B", "owned": True},
    ).json()
    return a["id"], b["id"]


def test_list_games_empty(client):
    r = client.get("/api/games")
    assert r.status_code == 200
    assert r.json() == []


def test_create_game(client, two_factions):
    fa_id, fb_id = two_factions
    r = client.post(
        "/api/games",
        json={
            "faction_a_id": fa_id,
            "faction_b_id": fb_id,
            "winner": "a",
            "player_a_name": "Alice",
            "player_b_name": "Bob",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["faction_a_id"] == fa_id
    assert data["faction_b_id"] == fb_id
    assert data["winner"] == "a"
    assert data["player_a_name"] == "Alice"
    assert data["player_b_name"] == "Bob"
    assert "played_at" in data
    assert "id" in data


def test_get_game(client, two_factions):
    fa_id, fb_id = two_factions
    cr = client.post(
        "/api/games",
        json={"faction_a_id": fa_id, "faction_b_id": fb_id, "winner": "b"},
    )
    gid = cr.json()["id"]
    r = client.get(f"/api/games/{gid}")
    assert r.status_code == 200
    assert r.json()["winner"] == "b"


def test_update_game(client, two_factions):
    fa_id, fb_id = two_factions
    cr = client.post(
        "/api/games",
        json={"faction_a_id": fa_id, "faction_b_id": fb_id, "winner": "a"},
    )
    gid = cr.json()["id"]
    r = client.put(
        f"/api/games/{gid}",
        json={"winner": "b"},
    )
    assert r.status_code == 200
    assert r.json()["winner"] == "b"


def test_delete_game(client, two_factions):
    fa_id, fb_id = two_factions
    cr = client.post(
        "/api/games",
        json={"faction_a_id": fa_id, "faction_b_id": fb_id, "winner": "a"},
    )
    gid = cr.json()["id"]
    r = client.delete(f"/api/games/{gid}")
    assert r.status_code == 204
    assert client.get(f"/api/games/{gid}").status_code == 404
