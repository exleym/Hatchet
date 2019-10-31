import datetime as dt
import logging
import pathlib
import re
import requests
from typing import List
from dateutil.parser import parse
from hatchet.client.team import Team, TeamClient
from hatchet.client.game import GameClient
from hatchet.util import load_csv


logger = logging.getLogger(__name__)
PATH = pathlib.Path(__file__).parent.parent / "hatchet/static/seeds/temp-games.csv"
UPLOAD_URL = 'http://localhost:5000/api/v1/games'
RANKING = re.compile(r"\([0-9]+\) ")
team_client = TeamClient()
game_client = GameClient()
__SR_CACHE = {}


def load_data(path: str) -> List[dict]:
    raw_data = load_csv(path, headers=True)
    return raw_data


def get_team(team_name: str) -> Team:
    global __SR_CACHE
    sanitized = re.sub(RANKING, "", team_name)
    team = __SR_CACHE.get(sanitized)
    if team:
        return team
    team = team_client.get_team_by_sr_id(sanitized)
    if not team:
        return None
    __SR_CACHE[sanitized] = team
    return team


def game_exists(school: Team, date: dt.date):
    if game_client.find_game(team_id=school.id, date=date):
        return True
    return False


def get_participants(game, school: Team, opponent: Team, stadium_id: int):
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


def loc_id(school: Team, opponent: Team, stadium_id: int):
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
        return None
    return school.stadium_id


def create_game(kickoff_time, stadium_id, participants):
    data = {
        "kickoffTime": kickoff_time.isoformat(),
        "stadiumId": stadium_id,
        "participants": participants
    }
    resp = requests.post(url=UPLOAD_URL, json=data)
    resp.raise_for_status()
    return resp.json()


def main():
    raw_data = load_data(PATH)
    for game in raw_data:
        kickoff = parse_kickoff_time(game)
        school = get_team(game.get("School"))
        opponent = get_team(game.get("Opponent"))
        if not opponent:
            logger.error(f"{game.get('Opponent')}")
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
        logger.info(new_game)
    logger.warning(f"added {len(raw_data)} games ...")


if __name__ == "__main__":
    main()
