def add_subdivisions(client):
    SUB = [
        {"code": "FBS", "name": "Football Bowl Subdivision", "division": 1},
        {"code": "FCS", "name": "Football Championship Subdivision", "division": 1},
    ]
    for s in SUB:
        client.post("/api/v1/subdivisions", json=s)
