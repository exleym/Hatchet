"""Primary client service for CFB Data API consumption

This client is designed to provide Hatchet CFB application
with programmatic access to the College Football Data API.


Key Links
---------
https://collegefootballdata.com/about
https://github.com/BlueSCar/cfb-api
"""
import requests
import hatchet.client.ext.cfb.schemas as schemas
import hatchet.util


class CFBDataClient(object):

    base_url = "https://api.collegefootballdata.com"
    game_schema = schemas.GameSchema()
    team_schema = schemas.TeamSchema()

    def __init__(self):
        pass

    def get_data(self, context: str, params: dict = None):
        url = f"{self.base_url}{context}"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def unwrap(self, data, schema):
        if isinstance(data, list):
            return schema.load(data, many=True)
        return schema.load(**data)

    def get_games(self, season: int):
        data = self.get_data("/games", {"year": season})
        return self.unwrap(data, schema=self.game_schema)

    def get_teams(self, conference: str = None, fbs_only: bool = False):
        params = {"conference": conference} if conference else {}
        context = "/teams"
        if fbs_only:
            context += "/fbs"
            params = {}
        data = self.get_data(context, params)
        return self.unwrap(data, schema=self.team_schema)


