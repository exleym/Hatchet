from hatchet.client.base import ResourceClient
from hatchet.client.hatchet_client import HatchetClient


hc = HatchetClient()


def test_hc_team_client():
    assert isinstance(hc.team_client, ResourceClient)


def test_hc_conf_client():
    assert isinstance(hc.conf_client, ResourceClient)


def test_hc_game_client():
    assert isinstance(hc.game_client, ResourceClient)


def test_hc_bookmaker_client():
    assert isinstance(hc.bookmaker_client, ResourceClient)


def test_hc_line_client():
    assert isinstance(hc.line_client, ResourceClient)


def test_week_client():
    assert isinstance(hc.week_client, ResourceClient)
