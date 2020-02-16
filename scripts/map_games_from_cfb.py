import logging
import requests
from typing import List
from hatchet.client.ext.cfb.client import CFBDataClient
from hatchet.client.hatchet_client import HatchetClient


SEASONS = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
logger = logging.getLogger(__name__)
cfb_client = CFBDataClient()
hatchet_client = HatchetClient(base_url="http://localhost:8000/api/v1")


def main(season: int):
    teams = cfb_client.get_teams(fbs_only=True)

    for team in teams:
        ht = hatchet_client.get_team_by_external_id(team.school, "CFB Data")
        hg = hatchet_client.get_team_games(ht.id, season=season)
        game_map = {game.game_time.date(): game for game in hg}
        games = cfb_client.get_games(season, team=team.school)
        for game in games:
            hatchet_game = game_map.get(game.game_date)
            if not hatchet_game:
                logger.error(f"no match for {game.home_team} on {game.start_date}!")
                continue
            hatchet_game.espn_id = game.id
            try:
                if not hatchet_game.rating:
                    hatchet_game.rating = None
                new_game = hatchet_client.update_game(hatchet_game)
                logger.info(f"added espn_id: {new_game.espn_id} to {new_game}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"unable to update {hatchet_game}.", e)




def run(seasons: List[int] = None):
    seasons = seasons or SEASONS
    for season in seasons:
        main(season)


if __name__ == "__main__":
    run()
