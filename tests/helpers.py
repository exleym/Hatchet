def add_subdivisions(client):
    SUB = [
        {"code": "FBS", "name": "Football Bowl Subdivision", "division": 1},
        {"code": "FCS", "name": "Football Championship Subdivision", "division": 1},
    ]
    for s in SUB:
        client.post("/api/v1/subdivisions", json=s)


def add_conferences(client):
    add_subdivisions(client)
    CONFERENCES = [
        (1, "AAA", "Alpha Conference", "Alpha", 1999),
        (1, "BBB", "Bravo Conference", "Bravo", 2000),
        (1, "CCC", "Charlie Conference", "Charlie", 2001),
        (2, "DDD", "Delta Conference", "Delta", 2002),
        (2, "EEE", "Echo Conference", "Echo", 2003),
        (2, "FFF", "Foxtrot Conference", "Foxtrot", 2004)
    ]
    for c in CONFERENCES:
        pkg = {
            "subdivisionId": c[0],
            "code": c[1],
            "name": c[2],
            "shortName": c[3],
            "inceptionYear": c[4]
        }
        client.post("/api/v1/conferences", json=pkg)
