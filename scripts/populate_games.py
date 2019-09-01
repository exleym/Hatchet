import logging
import requests

logger = logging.getLogger(__name__)

from hatchet import Environment
from hatchet.db.models import Game
from hatchet.resources.schemas import GameSchema, GameParticipantSchema, TeamSchema
from hatchet.util import load_csv


GAMES_PATH = '../hatchet/static/seeds/games.csv'
UPLOAD_URL = 'http://localhost:5000/api/v1/games'
TEAM_URL = 'http://localhost:5000/api/v1/teams'
PARTICIPANT_URL = 'http://localhost:5000/api/v1/games/{}/participants'


game_schema = GameSchema()
participant_schema = GameParticipantSchema()
team_schema = TeamSchema()


def main():
    raw_data = load_csv(GAMES_PATH, headers=True)
    game_fields = ['kickoffTime', 'stadiumId', 'espnId']
    for data in raw_data:
        game_package = {
            x: data.get(x) for x in game_fields
        }
        game = create_game(game_package)
        for team in ("team1", "team2"):
            team_name = data.get(team)
            location = int(data.get(f"{team}_loc"))
            score = int(data.get(f"{team}_score"))
            create_participant(game, team_name, location, score)


def create_game(data):
    if Environment.get() == Environment.TEST:
        json = {"id": 1, "kickoffTime": "2018-09-14T15:30:00",
                "stadiumId": 222, "espnId": 22222}
        logger.warning(f"creating participant {json} in TEST environment")
    else:
        resp = requests.post(url=UPLOAD_URL, json=data)
        json = resp.json()
    game = game_schema.load(json)
    logger.info(f"created game: {game}")
    return game


def create_participant(game: Game, team_name: str, location_type: int, score: int):
    team = get_team(team_name)
    if not team:
        return None
    package = {"teamId": team.id, "gameId": game.id, "locationTypeId": location_type,
               "score": score}
    if Environment.get() == Environment.TEST:
        package.update({"id": 98765})
        logger.warning(f"creating participant {package} in TEST environment")
    else:
        resp = requests.post(PARTICIPANT_URL.format(game.id), json=package)
        if resp.status_code != 201:
            logger.error(f"error posting {package}")
            logger.error(resp.content)
            return None
        package = resp.json()
    participant = participant_schema.load(package)
    logger.info(f"created participant {participant}")


def get_team(team_name):
    query = {"shortName": team_name}
    resp = requests.get(TEAM_URL, params=query)
    if resp.status_code != 200:
        return None
    team = resp.json()
    if team:
        return team_schema.load(team)
    return None


if __name__ == '__main__':
    Environment.set(Environment.TEST)
    main()
