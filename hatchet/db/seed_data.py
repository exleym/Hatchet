import logging
import pathlib
from hatchet.extensions import db
from hatchet.db.models import (
    Subdivision, Conference, Division, Stadium, Team, LocationType
)
from hatchet.db.crud.conferences import list_conferences
from hatchet.db.crud.divisions import list_divisions
from hatchet.db.crud.surfaces import list_surfaces, create_surface
from hatchet.db.crud.stadiums import list_stadiums
from hatchet.db.seeds.conferences import CONFERENCES
from hatchet.db.seeds.surfaces import SURFACES
from hatchet.util import load_csv

logger = logging.getLogger(__name__)
seed_path = pathlib.Path() / "hatchet" / "static" / "seeds"


def insert_seed_data():
    insert_surfaces()
    insert_location_types()
    insert_stadiums()
    insert_subdivisions()
    insert_conferences()
    insert_divisions()
    insert_teams()


def insert_subdivisions():
    data = [
        ("FBS", "Football Bowl Subdivision", 1),
        ("FCS", "Football Championship Subdivision", 1)
    ]
    for d in data:
        sd = Subdivision(code=d[0], name=d[1], division=d[2])
        db.session.add(sd)
        db.session.commit()
        logger.debug(f"added {sd} to database...")
    logger.warning(f"added subdivisions to database...")
    return 0


def insert_conferences():
    for c in CONFERENCES:
        conf = Conference(
            subdivision_id=c[0],
            code=c[1],
            name=c[2],
            short_name=c[3],
            inception_year=c[4]
        )
        db.session.add(conf)
        db.session.commit()
        logger.debug(f"added {conf} to database...")
    logger.warning(f"added conferences to database...")
    return 0


def insert_divisions():
    DIVS = seed_path / "divisions.csv"
    conferences = {c.code: c for c in list_conferences()}
    divisions = load_csv(DIVS, headers=True)
    for division in divisions:
        conf_code = division.pop("conference")
        conference = conferences.get(conf_code)
        div = Division(
            conference_id=conference.id,
            name=division.get("name")
        )
        db.session.add(div)
        db.session.commit()
        logger.debug(f"added {div} to database...")
    logger.warning(f"added divisions to database...")
    return 0


def insert_teams():
    TEAMS = seed_path / "teams.csv"
    conferences = {c.code: c for c in list_conferences()}
    divisions = {(d.conference.code, d.name): d for d in list_divisions()}
    stadiums = {s.code: s for s in list_stadiums()}
    raw_team_data = load_csv(TEAMS, headers=True)
    for t in raw_team_data:
        conf_code = t.pop("conference")
        div_name = t.pop("division")
        conf = conferences.get(conf_code)
        division = divisions.get((conf_code, div_name))
        stadium = stadiums.get(t.get("stadiumId"))
        team = Team(
            conference_id=conf.id,
            division_id=division.id,
            code=t.get("code"),
            name=t.get("name"),
            short_name=t.get("shortName"),
            mascot=t.get("mascot"),
            stadium_id=stadium.id if stadium else None
        )
        db.session.add(team)
        db.session.commit()
    logger.warning(f"added teams to database...")
    return 0


def insert_surfaces():
    for s in SURFACES:
        surf = create_surface(
            code=s[0],
            name=s[1],
            category=s[2]
        )
        logger.debug(f"added {surf} to database...")
    logger.warning("added surfaces to database...")


def insert_stadiums():
    STADIUMS = seed_path / "stadiums.csv"
    surfaces = {s.code: s for s in list_surfaces()}
    raw_stadiums = load_csv(STADIUMS, headers=True)
    for s in raw_stadiums:
        surface = surfaces.get(s.get("surface"))
        stadium = Stadium(
            code=s.get("code"),
            name=s.get("name"),
            state=s.get("state"),
            city=s.get("city"),
            longitude=s.get("longitude"),
            latitude=s.get("latitude"),
            built=s.get("built"),
            capacity=s.get("capacity"),
            surface_id=surface.id if surface else None
        )
        db.session.add(stadium)
        db.session.commit()
        logger.debug(f"creating {stadium} in db...")
    logger.warning(f"created stadiums in database...")
    return 0


def insert_location_types():
    LOC_TYPES = [
        LocationType(id=1, name="Home"),
        LocationType(id=2, name="Away"),
        LocationType(id=3, name="Neutral")
    ]
    for loc in LOC_TYPES:
        db.session.add(loc)
    db.session.commit()
    logger.warning(f"created {len(LOC_TYPES)} location types in database...")
    return 0