import logging
import pathlib
from hatchet.extensions import db
import hatchet.db.models as models
from hatchet.db.crud.base import create_resource, list_resources
from hatchet.db.seeds.conferences import CONFERENCES
from hatchet.db.seeds.surfaces import SURFACES
from hatchet.util import load_csv

logger = logging.getLogger(__name__)
seed_path = pathlib.Path() / "hatchet" / "static" / "seeds"


def insert_seed_data():
    insert_bookmakers()
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
        sd = create_resource(
            models.Subdivision,
            code=d[0],
            name=d[1],
            division=d[2]
        )
        logger.debug(f"added {sd} to database...")
    logger.warning(f"added subdivisions to database...")
    return 0


def insert_conferences():
    for c in CONFERENCES:
        conf = create_resource(
            models.Conference,
            subdivision_id=c[0],
            code=c[1],
            name=c[2],
            short_name=c[3],
            inception_year=c[4]
        )
        logger.debug(f"added {conf} to database...")
    logger.warning(f"added conferences to database...")
    return 0


def insert_divisions():
    DIVS = seed_path / "divisions.csv"
    conferences = {c.code: c for c in list_resources(models.Conference)}
    divisions = load_csv(DIVS, headers=True)
    for division in divisions:
        conf_code = division.pop("conference")
        conference = conferences.get(conf_code)
        div = create_resource(
            models.Division,
            conference_id=conference.id,
            name=division.get("name")
        )
        logger.debug(f"added {div} to database...")
    logger.warning(f"added divisions to database...")
    return 0


def insert_teams():
    TEAMS = seed_path / "teams.csv"
    conferences = {c.code: c for c in list_resources(models.Conference)}
    divisions = {
        (d.conference.code, d.name): d
        for d in list_resources(models.Division)
    }
    stadiums = {s.code: s for s in list_resources(models.Stadium)}
    raw_team_data = load_csv(TEAMS, headers=True)
    for t in raw_team_data:
        conf_code = t.pop("conference")
        div_name = t.pop("division")
        conf = conferences.get(conf_code)
        division = divisions.get((conf_code, div_name))
        stadium = stadiums.get(t.get("stadiumId"))
        team = create_resource(
            models.Team,
            conference_id=conf.id,
            division_id=division.id,
            code=t.get("code"),
            name=t.get("name"),
            short_name=t.get("shortName"),
            mascot=t.get("mascot"),
            stadium_id=stadium.id if stadium else None
        )
    logger.warning(f"added teams to database...")
    return 0


def insert_surfaces():
    for s in SURFACES:
        surf = create_resource(
            models.Surface,
            code=s[0],
            name=s[1],
            category=s[2]
        )
        logger.debug(f"added {surf} to database...")
    logger.warning("added surfaces to database...")


def insert_stadiums():
    STADIUMS = seed_path / "stadiums.csv"
    surfaces = {s.code: s for s in list_resources(models.Surface)}
    raw_stadiums = load_csv(STADIUMS, headers=True)
    for s in raw_stadiums:
        surface = surfaces.get(s.get("surface"))
        stadium = create_resource(
            models.Stadium,
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
        logger.debug(f"creating {stadium} in db...")
    logger.warning(f"created stadiums in database...")
    return 0


def insert_location_types():
    LOC_TYPES = [
        models.LocationType(id=1, name="Home"),
        models.LocationType(id=2, name="Away"),
        models.LocationType(id=3, name="Neutral")
    ]
    for loc in LOC_TYPES:
        db.session.add(loc)
    db.session.commit()
    logger.warning(f"created {len(LOC_TYPES)} location types in database...")
    return 0


def insert_bookmakers():
    BOOKMAKERS = [
        models.Bookmaker(code="BOV", name="Bovada", website="http://www.bovada.lv"),
        models.Bookmaker(code="FIVE", name="5Dimes", website="http://www.5dimes.eu"),
        models.Bookmaker(code="BM", name="BookMaker", website="http://www.bookmaker.eu"),
        models.Bookmaker(code="HRTG", name="Heritage Sports", website="http://www.heritagesports.eu")
    ]
    for bookie in BOOKMAKERS:
        db.session.add(bookie)
    db.session.commit()
    logger.warning(f"created bookmakers...")
    return 0
