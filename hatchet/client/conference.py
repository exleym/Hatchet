import dataclasses
import requests
from hatchet.client.base import BaseClient
import hatchet.resources.schemas.schemas as schemas
from hatchet.client.subdivision import Subdivision


schema = schemas.ConferenceSchema()


class SubdivisionClient(BaseClient):

    base_url = "http://localhost:5000/api/v1/teams"

    def __init__(self):
        pass

    def unwrap(self, data):
        if isinstance(data, list):
            return [self.unwrap(x) for x in data]
        data = schema.load(data)
        try:
            return Team(**data)
        except TypeError:
            return None

    def get_team(self, id: int = None, code: str = None):
        if id:
            return self.get_resource_by_id(id=id)
        return self.get_resource_by_code(code=code)

    def find(self, pattern: str) -> Team:
        teams = self.search(field="shortName", op="=", value=pattern)
        if not teams:
            teams = self.search(field="name", op="like", value=f"%{pattern}%")
        return self.unwrap(teams)

    def get_team_by_sr_id(self, name: str) -> Team:
        pkg = {"dataSource": "SportsReference", "teamName": name}
        resp = requests.post(f"{self.base_url}/external/search", json=pkg)
        if resp.status_code != 200:
            return None
        return self.unwrap(resp.json())
