from tests.helpers import add_subdivisions, add_conferences


def test_create_subdivision(client):
    pkg = {
        "code": "FBS",
        "name": "Football Bowl Subdivision",
        "division": 1
    }
    resp = client.post("/api/v1/subdivisions", json=pkg)
    pkg["id"] = 1

    assert resp.status_code == 201
    assert resp.json == pkg


def test_get_subdivisions(client):
    add_subdivisions(client)
    resp = client.get("/api/v1/subdivisions")
    assert len(resp.json) == 2


def test_get_subdivision_by_id(client):
    add_subdivisions(client)
    resp = client.get("/api/v1/subdivisions/2")
    assert resp.status_code == 200
    assert isinstance(resp.json, dict)
    assert resp.json == {
        "id": 2,
        "code": "FCS",
        "name": "Football Championship Subdivision",
        "division": 1
    }


def test_delete_subdivision(client):
    add_subdivisions(client)
    resp = client.get("/api/v1/subdivisions")
    assert len(resp.json) == 2
    resp = client.delete("/api/v1/subdivisions/1")
    assert resp.status_code == 204
    resp = client.get("/api/v1/subdivisions")
    assert len(resp.json) == 1


def test_subdivision_conferences(client):
    add_conferences(client)
    resp = client.get("/api/v1/subdivisions/1/conferences")

    assert resp.status_code == 200
    assert len(resp.json) == 3


# def test_missing_subdivision(client):
#     resp = client.get("/api/v1/subdivisions/3")
#     assert resp.json == {
#         "errors": [{"details": "", "message": "No Subdivision with id=4"}]
#     }