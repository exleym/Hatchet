import datetime
import hatchet.db.models as m


def test_subdivision_repr():
    s = m.Subdivision(code="A", name="B", division=1)
    assert str(s) == f"<Subdivision(id=None, code='A')>"


def test_subdivision_repr_with_id():
    s = m.Subdivision(id=1, code="A", name="B", division=1)
    assert str(s) == f"<Subdivision(id=1, code='A')>"


def test_surface_repr():
    surf = m.Surface(id=1, code="A", name="B", category="TURF")
    assert str(surf) == "<Surface(id=1, code='A', name='B')>"


def test_conference_repr():
    conf = m.Conference(
        id=10,
        subdivision_id=1,
        code="ACC",
        name="ACC",
        short_name="ACC",
        inception_year=1953
    )
    assert str(conf) == (f"<Conference(id=10, code='ACC', "
                         f"name='ACC', short_name='ACC')>")


def test_division_repr():
    div = m.Division(id=1, conference_id=1, name="Atlantic")
    assert str(div) == "<Division(id=1, conference_id=1, name='Atlantic')>"


def test_game_repr():
    game = m.Game(id=100, game_time=datetime.datetime.now(), stadium_id=7)
    assert str(game) == "<Game(id=100)>"
