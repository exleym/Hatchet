import dataclasses
import datetime
from typing import List


class Resource:
    pass


@dataclasses.dataclass
class Subdivision(Resource):
    id: int
    code: str
    name: str
    division: int


@dataclasses.dataclass
class Conference(Resource):
    id: int
    subdivision_id: int
    code: str
    name: str
    short_name: str
    inception_year: int
    subdivision: Subdivision


@dataclasses.dataclass
class Surface(Resource):
    id: int
    code: str
    name: str
    category: str


@dataclasses.dataclass
class Stadium(Resource):
    id: int
    code: str
    state: str
    city: str
    latitude: str
    longitude: str
    built: int
    capacity: int
    surfaceId: int
    surface: Surface = None


@dataclasses.dataclass
class Team(Resource):
    id: int
    code: str
    name: str
    short_name: str
    mascot: str
    conference_id: int
    division_id: int
    stadium_id: int
    stadium: Stadium = None


@dataclasses.dataclass
class Participant(Resource):
    team_id: int
    game_id: int
    location_type_id: int
    score: int
    team: Team = None


@dataclasses.dataclass
class Game(Resource):
    id: int
    game_time: datetime.datetime
    stadium_id: int
    espn_id: int
    participants: List[Participant]
    stadium: Stadium = None
