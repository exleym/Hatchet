import datetime as dt
import logging
import pathlib
import re
import requests
from typing import List
from dateutil.parser import parse
from hatchet.client.hatchet_client import HatchetClient
import hatchet.client.models as cm
from hatchet.util import load_csv


START_SEASON = 2000
END_SEASON = 2019
SEASONS = range(START_SEASON, END_SEASON + 1)
logger = logging.getLogger(__name__)
PATH = pathlib.Path(__file__).parent.parent / "hatchet/static/seeds/"
UPLOAD_URL = 'http://localhost:8000/api/v1/games'
RANKING = re.compile(r"\([0-9]+\) ")
client = HatchetClient(base_url="http://localhost:8000/api/v1")
__SR_CACHE = {}
__GAMES = set()


def load_data(path: str) -> List[dict]:
    raw_data = load_csv(path, headers=True)
    return raw_data


def get_team(team_name: str) -> cm.Team:
    global __SR_CACHE
    sanitized = re.sub(RANKING, "", team_name)
    team = __SR_CACHE.get(sanitized)
    if team:
        return team
    team = client.get_team_by_external_id(sanitized, source="SportsReference")
    if not team:
        return None
    __SR_CACHE[sanitized] = team
    return team


def game_exists(school: cm.Team, date: dt.date):
    game = frozenset([school.id, date])
    if game in __GAMES:
        return True
    return False


def get_participants(game, school: cm.Team, opponent: cm.Team, stadium_id: int):
    participants = []
    participants.append({
        "teamId": school.id,
        "locationTypeId": loc_id(school, opponent, stadium_id),
        "score": game.get("Pts")
    })
    participants.append({
        "teamId": opponent.id,
        "locationTypeId": loc_id(opponent, school, stadium_id),
        "score": game.get("Opp")
    })
    return participants


def loc_id(school: cm.Team, opponent: cm.Team, stadium_id: int):
    if school.stadium_id == stadium_id:
        return 1
    elif opponent.stadium_id == stadium_id:
        return 2
    return 3


def parse_kickoff_time(game):
    date = game.get("Date")
    time = game.get("Time")
    if time:
        return parse(f"{date} {time}")
    return parse(date)


def get_stadium(game, school, opponent):
    loc_type = game.get("LocType") or "h"
    if loc_type == "@":
        return opponent.stadium_id
    elif loc_type == "N":
        stadium_name = game.get("Notes")
        stadium = None
    return school.stadium_id


def create_game(kickoff_time, stadium_id, participants):
    data = {
        "kickoffTime": kickoff_time.isoformat(),
        "stadiumId": stadium_id,
        "participants": participants
    }
    resp = requests.post(url=UPLOAD_URL, json=data)
    if not resp.ok:
        logger.error(f"ERROR: {resp.json()}")
    resp.raise_for_status()
    return resp.json()


def main(season):
    f_in = f"games-{season}.csv"
    raw_data = load_data(PATH / f_in)
    for game in raw_data:
        kickoff = parse_kickoff_time(game)
        school = get_team(game.get("School"))
        opponent = get_team(game.get("Opponent"))
        if not opponent:
            logger.error(f"couldn't find {game.get('Opponent')} in Hatchet DB")
            continue
        if not school:
            logger.error(f"couldn't find {game.get('School')} in Hatchet DB")
            continue
        if game_exists(school, kickoff.date()):
            logger.info(f"{school.short_name} / {opponent.short_name} already exists...")
            continue
        stadium_id = get_stadium(game=game, school=school, opponent=opponent)
        new_game = create_game(
            kickoff_time=kickoff,
            stadium_id=stadium_id,
            participants=get_participants(game, school, opponent, stadium_id)
        )
        __GAMES.add(frozenset([school.id, kickoff.date()]))
        __GAMES.add(frozenset([opponent.id, kickoff.date()]))
        logger.info(new_game)
    logger.warning(f"added {len(raw_data)} games for season {season}...")


def run(seasons: List[int] = None):
    seasons = seasons or SEASONS
    for season in seasons:
        main(season=season)


if __name__ == "__main__":
    run()
