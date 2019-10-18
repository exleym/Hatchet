import dataclasses
import requests
from hatchet.client.base import BaseClient
from hatchet.util import camel_to_snake


@dataclasses.dataclass
class Team:
    id: int
    code: str
    name: str
    short_name: str
    mascot: str
    conference_id: int
    division_id: int
    stadium_id: int


class TeamClient(BaseClient):

    base_url = "http://localhost:5000/api/v1/teams"

    def __init__(self):
        pass

    def unwrap(self, data):
        data = camel_to_snake(data)
        return Team(**data)

    def get_team(self, id: int = None, code: str = None):
        if id:
            return self.get_resource_by_id(id=id)
        return self.get_resource_by_code(code=code)
