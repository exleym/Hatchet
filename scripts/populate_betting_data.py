import logging
from typing import List
from hatchet.client.ext.cfb.client import CFBDataClient
from hatchet.client.hatchet_client import HatchetClient
from hatchet.errors import MissingResourceException

logger = logging.getLogger(__name__)

SEASONS = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
CFBD = "CFB Data"
cfb_client = CFBDataClient()
hct_client = HatchetClient(base_url="http://localhost:8000/api/v1")


def main(season, week: int = None):
    game_lines = cfb_client.get_lines(season=season, week=week)
    bookies = {b.name.lower(): b for b in hct_client.get_bookmakers()}

    for game in game_lines:

        # Get Home & Away Teams. CFB Data API displays all spreads as relative
        # to the home team. We will save home and away spreads (+1 / -1)
        home_team = hct_client.get_team_by_external_id(
            name=game.home_team,
            source=CFBD
        )
        away_team = hct_client.get_team_by_external_id(
            name=game.away_team,
            source=CFBD
        )
        try:
            hatchet_game = hct_client.get_game(espn_id=game.id)
        except MissingResourceException:
            logger.error(f"No game matches espn id = {game.id}")
            continue

        for line in game.lines:
            bookie = bookies.get(line.provider.lower())
            if not line.spread:
                logger.error(f"no spread for line {line}")
                continue

            over_under = float(line.over_under) if line.over_under else None
            spread = float(line.spread) if line.spread else None

            if home_team:
                hct_client.create_line(
                    game_id=hatchet_game.id,
                    team_id=home_team.id,
                    bookmaker_id=bookie.id,
                    spread=spread,
                    over_under=over_under,
                    vigorish=None
                )
            if away_team:
                spread = float(line.spread)
                hct_client.create_line(
                    game_id=hatchet_game.id,
                    team_id=away_team.id,
                    bookmaker_id=bookie.id,
                    spread=spread*-1 if spread else None,
                    over_under=over_under,
                    vigorish=None
                )
        logger.info(f"added {len(game.lines)} lines for {game}")


def run(seasons: List[int] = None):
    seasons = seasons or SEASONS
    hct_client.clear_lines()
    for season in seasons:
        main(season=season)


if __name__ == "__main__":
    run()
