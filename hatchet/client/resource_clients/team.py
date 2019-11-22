import datetime as dt
import logging
import requests
from typing import List
from hatchet.client.hatchet_client import ResourceClient
import hatchet.client.models as cm
import hatchet.client.schemas as schemas



logger = logging.getLogger(__name__)


class TeamClient(ResourceClient):

    game_schema = schemas.ClientGameSchema()

    def get_team_by_external_id(self, name: str, source: str):
        pkg = {"dataSource": source, "teamName": name}
        try:
            data = self.post_data(
                f"{self.base_url}/external/search", body=pkg
            )
            team = self.unwrap(data)
            return team
        except requests.exceptions.HTTPError:
            logger.error(f"no Team with id={name} for source={source}...")
        team = None
        return team

    def get_team_games(self, team_id: int, season: int = None,
                       date: dt.date = None) -> List[cm.Game]:
        url = f"{self.base_url}/{team_id}/games"
        params = {}
        if season: params.update({"season": season})
        if date: params.update({"date": date.isoformat()})
        data = self.get_data(url=url, params=params)
        return self.game_schema.load(data, many=True)
