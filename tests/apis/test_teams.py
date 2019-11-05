from tests.helpers import add_divisions, add_teams, add_stadiums


def test_create_team(client):
    add_stadiums(client)
    add_divisions(client)
    pkg = {
        "code": "CLEM",
        "name": "Clemson University",
        "shortName": "Clemson",
        "mascot": "Tigers",
        "conferenceId": 1,
        "divisionId": 1,
        "stadiumId": None
    }
    resp = client.post("/api/v1/teams", json=pkg)

    assert resp.json.get("id") == 1
    assert resp.status_code == 201



def test_get_teams(client):
    add_teams(client)
    resp = client.get("/api/v1/teams")
    assert len(resp.json) == 10


def test_get_team_by_id(client):
    add_teams(client)
    resp = client.get("/api/v1/teams/2")
    assert resp.status_code == 200
    assert isinstance(resp.json, dict)
    assert resp.json.get("id") == 2


def test_delete_team(client):
    add_teams(client)
    resp = client.get("/api/v1/teams")
    assert len(resp.json) == 10
    resp = client.delete("/api/v1/teams/1")
    assert resp.status_code == 204
    resp = client.get("/api/v1/teams")
    assert len(resp.json) == 9


# def test_team_games(client):
#     add_teams(client)
#     resp = client.get("/api/v1/subdivisions/1/conferences")
#
#     assert resp.status_code == 200
#     assert len(resp.json) == 3


# def test_missing_subdivision(client):
#     resp = client.get("/api/v1/subdivisions/3")
#     assert resp.json == {
#         "errors": [{"details": "", "message": "No Subdivision with id=4"}]
#     }