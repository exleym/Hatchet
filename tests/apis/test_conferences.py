from tests.helpers import add_conferences, add_subdivisions


def test_create_conference(client):
    add_subdivisions(client)
    pkg = {
        "subdivisionId": 1,
        "code": "ACC",
        "name": "Atlantic Coast Conference",
        "shortName": "ACC",
        "inceptionYear": 1953
    }
    resp = client.post("/api/v1/conferences", json=pkg)
    subdivision = client.get("/api/v1/subdivisions/1")
    pkg["id"] = 1
    pkg["subdivision"] = subdivision.json
    assert resp.status_code == 201
    assert resp.json == pkg


def test_get_conferences(client):
    add_conferences(client)
    resp = client.get("/api/v1/conferences")
    assert resp.status_code == 200
    assert len(resp.json) == 6


def test_get_conference_by_id(client):
    add_conferences(client)
    resp = client.get("/api/v1/conferences/3")
    assert resp.status_code == 200
    assert resp.json.get("id") == 3


def test_update_conference(client):
    add_conferences(client)
    resp = client.get("/api/v1/conferences/4")
    data = resp.json
    sub = data.pop("subdivision")
    data["code"] = "XYZ"
    resp = client.put("/api/v1/conferences/4", json=data)
    data["subdivision"] = sub
    assert resp.status_code == 200
    assert resp.json == data
