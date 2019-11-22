from tests.helpers import add_networks, add_ratings, add_games


def test_empty_ratings_query(client):
    resp = client.get("/api/v1/ratings")
    assert resp.json == []


def test_create_minimal_rating(client):
    add_games(client)
    add_networks(client)
    rtg = {"gameId": 1, "networkId": 1, "rating": 0.9, "viewers": 4.5}
    resp = client.post("/api/v1/ratings", json=rtg)
    assert resp.json == {
        "id": 1,
        "gameId": 1,
        "networkId": 1,
        "rating": '0.9',
        "viewers": '4.5'
    }


def test_adding_ratings_propagates_to_fetch(client):
    add_ratings(client)
    resp = client.get("/api/v1/ratings")
    assert len(resp.json) == 5


def test_rating_update(client):
    add_ratings(client)
    pkg = {"rating": 0.75, "viewers": 10.5}
    client.put("/api/v1/ratings/1", json=pkg)
    resp = client.get("/api/v1/ratings/1")
    pkg["id"] = 1
    pkg["gameId"] = 1
    pkg["networkId"] = 1
    pkg["rating"] = str(pkg["rating"])
    pkg["viewers"] = str(pkg["viewers"])
    assert resp.json == pkg


def test_rating_delete(client):
    add_ratings(client)
    client.delete("/api/v1/ratings/1")
    resp = client.get("/api/v1/ratings")
    assert len(resp.json) == 4


def test_rating_not_found_response(client):
    resp = client.get("/api/v1/ratings/3")
    assert resp.status_code == 404
    assert resp.json == {
    "errors": [
        {
          "details": "MissingResourceException: No Rating with id=3",
          "message": "No Rating with id=3"
        }
      ]
    }


def test_delete_missing_rating_response(client):
    resp = client.delete("/api/v1/ratings/1")
    assert resp.status_code == 404
    assert resp.json == {
    "errors": [
        {
          "details": "MissingResourceException: No Rating with id=1",
          "message": "No Rating with id=1"
        }
      ]
    }
