def test_list_factions_empty(client):
    r = client.get("/api/factions")
    assert r.status_code == 200
    assert r.json() == []


def test_create_faction(client):
    r = client.post(
        "/api/factions",
        json={"name": "Phoenix Elves", "summoner_name": "Maelorn", "owned": True},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Phoenix Elves"
    assert data["summoner_name"] == "Maelorn"
    assert data["owned"] is True
    assert "id" in data


def test_get_faction(client):
    cr = client.post(
        "/api/factions",
        json={"name": "Cave Goblins", "summoner_name": "Screetch"},
    )
    fid = cr.json()["id"]
    r = client.get(f"/api/factions/{fid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Cave Goblins"


def test_get_faction_404(client):
    r = client.get("/api/factions/99999")
    assert r.status_code == 404


def test_update_faction(client):
    cr = client.post(
        "/api/factions",
        json={"name": "Old", "summoner_name": "Summoner", "owned": False},
    )
    fid = cr.json()["id"]
    r = client.put(
        f"/api/factions/{fid}",
        json={"name": "Updated", "owned": True},
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Updated"
    assert r.json()["owned"] is True


def test_delete_faction(client):
    cr = client.post(
        "/api/factions",
        json={"name": "ToDelete", "summoner_name": "Del"},
    )
    fid = cr.json()["id"]
    r = client.delete(f"/api/factions/{fid}")
    assert r.status_code == 204
    assert client.get(f"/api/factions/{fid}").status_code == 404


def test_list_factions_filter_owned(client):
    client.post("/api/factions", json={"name": "A", "summoner_name": "S1", "owned": True})
    client.post("/api/factions", json={"name": "B", "summoner_name": "S2", "owned": False})
    r = client.get("/api/factions?owned=true")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "A"
