from dateutil.parser import parse
import logging
import pathlib
from typing import List
from hatchet.client.ext.cfb.client import CFBDataClient
from hatchet.client.hatchet_client import HatchetClient
from hatchet.errors import MissingResourceException
from hatchet.util import load_csv


logger = logging.getLogger(__name__)


# SEASONS = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
SEASONS = [2016, 2017, 2018]
CFBD = "CFB Data"
PATH = pathlib.Path(__file__).parent.parent / "hatchet/static/seeds/"
cfb_client = CFBDataClient()
hct_client = HatchetClient()
__TEAMS = {}
__NETWORKS = {}


def load_data(path: str) -> List[dict]:
    raw_data = load_csv(path, headers=True)
    return raw_data


def main(season: int):
    f_in = f"ratings-{season}.csv"
    raw_data = load_data(PATH / f_in)
    teams = hct_client.list_teams()
    networks = hct_client.list_networks()
    __TEAMS.update({t.code: t for t in teams})
    __NETWORKS.update({n.code: n for n in networks})
    for rtg in raw_data:
        team = __TEAMS.get(rtg.get("team"))
        network = __NETWORKS.get(rtg.get("network"))
        if not team:
            logger.error(f"no team with code={rtg.get('team')}")
            continue
        if not network:
            logger.error(f"no network with code={rtg.get('network')}")
            continue
        date = parse(rtg.get("date")).date()
        game = hct_client.find_game(team_id=team.id, date=date)
        if not game:
            logger.error(f"no game found matching {team.short_name} on {date}")
            continue
        hct_client.create_rating(
            game_id=game.id,
            network_id=network.id,
            rating=rtg.get("rating"),
            viewers=rtg.get("viewers")
        )


def run(seasons: List[int] = None):
    seasons = seasons or SEASONS
    for season in seasons:
        main(season=season)


if __name__ == "__main__":
    run()
