import dataclasses
import datetime
from typing import List


@dataclasses.dataclass
class Game:
    id: str
    season: int
    week: int
    season_type: str
    start_date: datetime.datetime
    neutral_site: bool
    conference_game: bool
    attendance: float
    venue_id: int
    venue: str
    home_team: str
    home_conference: str
    home_points: int
    home_line_scores: List[int]
    away_team: str
    away_conference: str
    away_points: int
    away_line_scores: List[int]


@dataclasses.dataclass
class Team:
    id: int
    school: str
    mascot: str
    abbreviation: str
    alt_name_1: str
    alt_name_2: str
    alt_name_3: str
    conference: str
    division: str
    color: str
    alt_color: str
    logos: List[str]
