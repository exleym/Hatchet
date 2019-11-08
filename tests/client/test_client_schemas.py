import datetime
from marshmallow.exceptions import ValidationError
import pytest
import hatchet.client.schemas as cs
import hatchet.client.models as cm


def test_client_bookmaker_schema_load():
    schema = cs.ClientBookmakerSchema()
    data = {
        "id": 13,
        "code": "BOV",
        "name": "Bovada",
        "website": "http://bova.da"
    }
    bov = schema.load(data)
    assert isinstance(bov, cm.Bookmaker)
    assert bov == cm.Bookmaker(
        id=13, code="BOV", name="Bovada", website="http://bova.da"
    )


def test_client_subdivision_schema_load():
    schema = cs.ClientSubdivisionSchema()
    data = {
        "id": 1,
        "code": "FBS",
        "name": "FootBallS",
        "division": 1
    }
    fbs = schema.load(data)
    assert isinstance(fbs, cm.Subdivision)
    assert fbs == cm.Subdivision(
        id=1, code="FBS", name="FootBallS", division=1
    )


def test_client_surface_schema_load():
    schema = cs.ClientSurfaceSchema()
    data = {
        "id": 2,
        "code": "TIF-419",
        "name": "Tifway",
        "category": "Grass"
    }
    surf = schema.load(data)
    assert surf == cm.Surface(
        id=2, code="TIF-419", name="Tifway", category="Grass"
    )


def test_client_stadium_schema_load():
    schema = cs.ClientStadiumSchema()
    data = {
        "id": 3,
        "code": "DV",
        "name": "Clemson Memorial",
        "state": "SC",
        "city": "Clemson",
        "latitude": "25N",
        "longitude": "38W",
        "built": 1960,
        "capacity": 82_500,
        "surfaceId": 1,
        "surface": {
            "id": 1,
            "code": "TIF-419",
            "name": "Tifway",
            "category": "Grass"
        }
    }
    stadium = schema.load(data)
    assert isinstance(stadium, cm.Stadium)
    assert isinstance(stadium.surface, cm.Surface)
    assert stadium.surface_id == stadium.surface.id


def test_stadium_loads_without_surface():
    schema = cs.ClientStadiumSchema()
    data = {
        "id": 3,
        "code": "DV",
        "name": "Clemson Memorial",
        "state": "SC",
        "city": "Clemson",
        "latitude": "25N",
        "longitude": "38W",
        "built": 1960,
        "capacity": 82_500,
        "surfaceId": 1
    }
    stadium = schema.load(data)
    assert isinstance(stadium, cm.Stadium)
    assert stadium.surface is None


def test_client_conference_schema_load():
    schema = cs.ClientConferenceSchema()
    data = {
        "id": 10,
        "subdivisionId": 1,
        "code": "MPC",
        "name": "Test",
        "shortName": "TST",
        "inceptionYear": 1990,
        "subdivision": {
            "id": 1,
            "code": "FBS",
            "name": "FootBallS",
            "division": 1
        }
    }
    conf = schema.load(data)
    assert isinstance(conf, cm.Conference)
    assert isinstance(conf.subdivision, cm.Subdivision)
    assert conf.id == 10
    assert conf.subdivision_id == conf.subdivision.id


def test_client_conference_loads_without_subdivision():
    schema = cs.ClientConferenceSchema()
    data = {
        "id": 10,
        "subdivisionId": 1,
        "code": "MPC",
        "name": "Test",
        "shortName": "TST",
        "inceptionYear": 1990,
    }
    conf = schema.load(data)
    assert isinstance(conf, cm.Conference)
    assert conf.subdivision is None


def test_conference_schema_raises_validation_error_for_old_year():
    schema = cs.ClientConferenceSchema()
    data = {
        "id": 10, "subdivisionId": 1, "code": "MPC",
        "name": "Test", "shortName": "TST", "inceptionYear": 1879,
    }
    with pytest.raises(ValidationError):
        schema.load(data)


def test_conference_schema_raises_validation_error_for_future_year():
    T_PLUS_1 = datetime.date.today().year + 1
    schema = cs.ClientConferenceSchema()
    data = {
        "id": 10, "subdivisionId": 1, "code": "MPC",
        "name": "Test", "shortName": "TST", "inceptionYear": T_PLUS_1,
    }
    with pytest.raises(ValidationError):
        schema.load(data)


def test_client_team_schema_load():
    schema = cs.ClientTeamSchema()
    data = {
        "id": 42,
        "code": "CLEM",
        "name": "Clemson",
        "shortName": "Clemson",
        "mascot": "Tigers",
        "conferenceId": 1,
        "divisionId": 1,
        "stadiumId": 1
    }
    team = schema.load(data)
    assert isinstance(team, cm.Team)
    assert team.stadium is None
    assert team.division is None


def test_client_team_schema_loads_with_division():
    schema = cs.ClientTeamSchema()
    data = {
        "id": 42,
        "code": "CLEM",
        "name": "Clemson",
        "shortName": "Clemson",
        "mascot": "Tigers",
        "conferenceId": 1,
        "divisionId": 3,
        "stadiumId": 1,
        "division": {
            "id": 3,
            "conferenceId": 1,
            "name": "ACC Atlantic"
        }
    }
    team = schema.load(data)
    assert isinstance(team, cm.Team)
    assert isinstance(team.division, cm.Division)
