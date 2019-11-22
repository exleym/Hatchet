from tests.helpers import add_networks


def test_empty_networks_query(client):
    resp = client.get("/api/v1/networks")
    assert resp.json == []


def test_create_minimal_networks(client):
    network = {"code": "TEST", "name": "TEST-NAME", "website": None}
    resp = client.post("/api/v1/networks", json=network)
    assert resp.json == {
        "id": 1,
        "code": "TEST",
        "name": "TEST-NAME",
        "website": None
    }


def test_adding_networks_propagates_to_fetch(client):
    add_networks(client)
    resp = client.get("/api/v1/networks")
    assert len(resp.json) == 2


def test_network_update(client):
    add_networks(client)
    pkg = {"code": "Foo", "name": "bar", "website": "http://baz.io"}
    client.put("/api/v1/networks/1", json=pkg)
    resp = client.get("/api/v1/networks/1")
    pkg["id"] = 1
    assert resp.json == pkg


def test_network_delete(client):
    add_networks(client)
    client.delete("/api/v1/networks/1")
    resp = client.get("/api/v1/networks")
    assert len(resp.json) == 1


def test_network_not_found_response(client):
    resp = client.get("/api/v1/networks/3")
    assert resp.status_code == 404
    assert resp.json == {
    "errors": [
        {
          "details": "MissingResourceException: No Network with id=3",
          "message": "No Network with id=3"
        }
      ]
    }


def test_delete_missing_network_response(client):
    resp = client.delete("/api/v1/networks/1")
    assert resp.status_code == 404
    assert resp.json == {
    "errors": [
        {
          "details": "MissingResourceException: No Network with id=1",
          "message": "No Network with id=1"
        }
      ]
    }
