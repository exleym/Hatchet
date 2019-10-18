import dataclasses
import datetime
import requests
from hatchet.client.base import BaseClient
from hatchet.apis.schemas import GameSchema
from hatchet.util import camel_to_snake
from typing import List, Dict


@dataclasses.dataclass
class Game:
    id: int
    game_time: datetime.datetime
    stadium_id: int
    espn_id: int
    participants: List
    winner: Dict


class GameClient(BaseClient):

    base_url = "http://localhost:5000/api/v1/games"
    team_base_url = "http://localhost:5000/api/v1/teams/{}/games"
    schema = GameSchema()

    def __init__(self):
        pass

    def unwrap(self, data):
        return Game(**self.schema.load(data))

    def get_game(self, id: int):
        return self.get_resource_by_id(id=id)

    def get_team_games(self, team_id: int, season: int = None):
        if not season:
            season = datetime.date.today().year
        url = self.team_base_url.format(team_id)
        games = self.get_data(url=url, params={"season": season})
        return [self.unwrap(x) for x in games]

    def find_game(self, team_id: int, date: datetime.date):
        games = self.get_team_games(team_id=team_id, season=date.year)
        match = [g for g in games if g.game_time.date() == date]
        if match:
            return match[0]
        return None