import dataclasses
import datetime
import pytz
from typing import List


class Resource:
    pass


@dataclasses.dataclass
class Bookmaker(Resource):
    id: int
    code: str
    name: str
    website: str


@dataclasses.dataclass
class DataSource(Resource):
    id: int
    code: str
    name: str
    url: str


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
    inception_year: int = None
    subdivision: Subdivision = None


@dataclasses.dataclass
class Division(Resource):
    id: int
    conference_id: int
    name: str = None
    conference: Conference = None


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
    name: str
    state: str
    city: str
    latitude: str
    longitude: str
    built: int
    capacity: int
    surface_id: int = None
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
    stadium_id: int = None
    stadium: Stadium = None
    division: Division = None


@dataclasses.dataclass
class Participant(Resource):
    id: int
    team_id: int
    game_id: int
    location_type_id: int
    score: int
    team: Team = None


@dataclasses.dataclass
class Week:
    id: int
    number: int
    season: int
    start_date: datetime.date
    end_date: datetime.date


@dataclasses.dataclass
class Network:
    id: int
    code: str
    name: str
    website: str


@dataclasses.dataclass
class Rating:
    id: int
    game_id: int
    network_id: int
    rating: float
    viewers: float


@dataclasses.dataclass
class Game(Resource):
    id: int
    game_time: datetime.datetime
    stadium_id: int
    espn_id: int
    participants: List[Participant] = None
    winner: Participant = None
    stadium: Stadium = None
    rating: Rating = None


@dataclasses.dataclass
class Line(Resource):
    id: int
    game_id: int
    team_id: int
    bookmaker_id: int
    spread: float
    over_under: float
    vigorish: int
    game: Game = None
    team: Team = None
    bookmaker: Bookmaker = None
