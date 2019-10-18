import datetime
from dateutil.parser import parse
import logging
import requests

logger = logging.getLogger(__name__)

from hatchet import Environment
from hatchet.client.team import TeamClient, Team
from hatchet.client.game import GameClient
from hatchet.util import load_csv


GAMES_PATH = '../hatchet/static/seeds/games.csv'
UPLOAD_URL = 'http://localhost:5000/api/v1/games'
PARTICIPANT_URL = 'http://localhost:5000/api/v1/games/{}/participants'


team_client = TeamClient()
game_client = GameClient()


def main():
    raw_data = load_csv(GAMES_PATH, headers=True)
    for game in raw_data:
        kickoff = parse(f"{game.get('Date')} {game.get('Time')}")
        school = team_client.get_team(code=game["School"])
        opponent = team_client.get_team(code=game["Opponent"])
        if game_exists(school, kickoff.date()):
            logger.warning(f"{school.short_name} / {opponent.short_name} already exists...")
            continue
        stadium_id = get_stadium(game=game, school=school, opponent=opponent)
        new_game = create_game(
            kickoff_time=kickoff,
            stadium_id=stadium_id,
            participants=get_participants(game, school, opponent, stadium_id)
        )
        logger.info(new_game)


def game_exists(school: Team, date: datetime.date):
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


def get_stadium(game, school, opponent):
    loc_type = game.get("LocType") or "h"
    if loc_type == "@":
        return opponent.stadium_id
    elif loc_type == "h":
        return school.stadium_id
    return None


def create_game(kickoff_time, stadium_id, participants):
    data = {
        "kickoffTime": kickoff_time.isoformat(),
        "stadiumId": stadium_id,
        "participants": participants
    }
    resp = requests.post(url=UPLOAD_URL, json=data)
    resp.raise_for_status()
    return resp.json()


if __name__ == '__main__':
    Environment.set(Environment.TEST)
    main()
