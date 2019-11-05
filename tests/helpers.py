def add_subdivisions(client):
    SUB = [
        {"code": "FBS", "name": "Football Bowl Subdivision", "division": 1},
        {"code": "FCS", "name": "Football Championship Subdivision", "division": 1},
    ]
    for s in SUB:
        client.post("/api/v1/subdivisions", json=s)


def add_conferences(client, limit: int = None):
    add_subdivisions(client)
    CONFERENCES = [
        (1, "AAA", "Alpha Conference", "Alpha", 1999),
        (1, "BBB", "Bravo Conference", "Bravo", 2000),
        (1, "CCC", "Charlie Conference", "Charlie", 2001),
        (2, "DDD", "Delta Conference", "Delta", 2002),
        (2, "EEE", "Echo Conference", "Echo", 2003),
        (2, "FFF", "Foxtrot Conference", "Foxtrot", 2004)
    ]
    if limit: CONFERENCES = CONFERENCES[:limit] # optionally reduce count
    for c in CONFERENCES:
        pkg = {
            "subdivisionId": c[0],
            "code": c[1],
            "name": c[2],
            "shortName": c[3],
            "inceptionYear": c[4]
        }
        client.post("/api/v1/conferences", json=pkg)


def add_divisions(client):
    add_conferences(client, limit=2)
    DIVISIONS = [
        (1, "Alpha East"),
        (1, "Alpha West"),
        (2, "Bravo North"),
        (2, "Bravo South")
    ]
    for div in DIVISIONS:
        pkg = {
            "conferenceId": div[0],
            "name": div[1]
        }
        client.post("/api/v1/divisions", json=pkg)


def add_teams(client, limit: int = None):
    add_divisions(client)
    TEAMS = [
        ("ASU", "America State University", "America State", "Apples", 1, 1, 1),
        ("BSU", "Big State University", "Big State", "Bananas", 1, 1, 2),
        ("CSU", "Corny State University", "Corny State", "Corns", 1, 1, 3),
        ("DSU", "Donkeytown State University", "Donkeytown", "Donkeys", 1, 2, 4),
        ("ESU", "Enemy State University", "Enemy State", "Elephants", 1, 2, 5),
        ("FSU", "Failed State University", "Failed State", "Failures", 1, 2, 6),
        ("GSU", "Garden State University", "Garden State", "Guidos", 2, 3, 7),
        ("HSU", "Holy State University", "Holy State", "Hannibals", 2, 3, 8),
        ("ISU", "Irish State University", "Irish State", "Leprechauns", 2, 3, 9),
        ("JSU", "Jerry State University", "Jerry State", "Jerries", 2, 3, 10)
    ]
    if limit: TEAMS = TEAMS[:limit]
    for t in TEAMS:
        pkg = {
            "code": t[0],
            "name": t[1],
            "shortName": t[2],
            "mascot": t[3],
            "conferenceId": t[4],
            "divisionId": t[5],
            "stadiumId": t[6]
        }
        client.post("/api/v1/teams", json=pkg)


def add_stadiums(client):
    STADIUMS = [
        ("S1", "Stadium 1", "AL", "Hottown", None, None, 1900, 100000, None, None),
        ("S2", "Stadium 2", "AK", "Coldtown", None, None, 1901, 100000, None, None)
    ]
    for s in STADIUMS:
        pkg = {
            "code": s[0],
            "name": s[1],
            "state": s[2],
            "city": s[3],
            "latitude": None,
            "longitude": None,
            "build": s[6],
            "capacity": s[7],
            "surfaceId": None
        }
        client.post("/api/v1/stadiums", json=pkg)
