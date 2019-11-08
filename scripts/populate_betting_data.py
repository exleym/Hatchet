import logging
from hatchet.client.ext.cfb.client import CFBDataClient
from hatchet.client.hatchet_client import HatchetClient


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

SEASONS = [2019]
CFBD = "CFB Data"
cfb_client = CFBDataClient()
hct_client = HatchetClient()


def main(season, week):
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
        hatchet_game = hct_client.get_game(espn_id=game.id)

        for line in game.lines:
            bookie = bookies.get(line.provider.lower())
            if not line.spread:
                logger.error(f"no spread for line {line}")
                continue
            hct_client.create_line(
                game_id=hatchet_game.id,
                team_id=home_team.id,
                bookmaker_id=bookie.id,
                spread=float(line.spread),
                over_under=float(line.over_under),
                vigorish=None
            )
            if away_team:
                hct_client.create_line(
                    game_id=hatchet_game.id,
                    team_id=away_team.id,
                    bookmaker_id=bookie.id,
                    spread=float(line.spread)*-1,
                    over_under=float(line.over_under),
                    vigorish=None
                )
        logger.warning(f"added {len(game.lines)} lines for {game}")


if __name__ == "__main__":
    hct_client.clear_lines()
    for season in SEASONS:
        weeks = hct_client.list_weeks(season=season)
        for week in weeks:
            main(season=season, week=week.number)
