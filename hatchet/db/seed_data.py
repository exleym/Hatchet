import dateutil.parser as parser
import logging
import pathlib
import re
from hatchet.extensions import db
import hatchet.db.models as models
import hatchet.db.meta_models as meta
from hatchet.db.queries.lookups import lookup_team_by_external_id
from hatchet.db.crud.base import create_resource, list_resources
from hatchet.db.seeds.conferences import CONFERENCES
from hatchet.db.seeds.data_sources import DATA_SOURCES
from hatchet.db.seeds.surfaces import SURFACES
import hatchet.util as util

logger = logging.getLogger(__name__)
# team_client = TeamClient()
seed_path = pathlib.Path() / "hatchet" / "static" / "seeds"


def insert_seed_data():
    conf = list_resources(model=models.Conference)
    if conf:
        return None
    insert_weeks()
    insert_data_sources()
    insert_bookmakers()
    insert_surfaces()
    insert_location_types()
    insert_stadiums()
    insert_subdivisions()
    insert_conferences()
    insert_divisions()
    insert_teams()
    insert_team_mappers()
    insert_polls()
    insert_rankings()


def insert_weeks():
    WEEKS = seed_path / "weeks.csv"
    weeks = util.load_csv(WEEKS, headers=True)
    for week in weeks:
        week["start_date"] = parser.parse(week["start_date"]).date()
        week["end_date"] = parser.parse(week["end_date"]).date()
        db.session.add(models.Week(**week))
    db.session.commit()
    logger.warning(f"created weeks for rankings...")
    return 0


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
    divisions = util.load_csv(DIVS, headers=True)
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
    raw_team_data = util.load_csv(TEAMS, headers=True)
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


def insert_data_sources():
    for ds in DATA_SOURCES:
        create_resource(
            meta.DataSource,
            code=ds.code,
            name=ds.name,
            url=ds.url
        )


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
    raw_stadiums = util.load_csv(STADIUMS, headers=True)
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
        models.Bookmaker(code="HRTG", name="Heritage Sports", website="http://www.heritagesports.eu"),
        models.Bookmaker(code="CEZ", name="Caesars", website=""),
        models.Bookmaker(code="CONS", name="Consensus", website=""),
        models.Bookmaker(code="NF", name="numberfire", website=""),
        models.Bookmaker(code="TR", name="teamrankings", website=""),
    ]
    for bookie in BOOKMAKERS:
        db.session.add(bookie)
    db.session.commit()
    logger.warning(f"created bookmakers...")
    return 0


def insert_team_mappers():
    SR_TEAM_MAPPING = seed_path / "sr-team-mapping.csv"
    ESPN_TEAM_MAPPING = seed_path / "espn-team-mapping.csv"
    CFBDATA_TEAM_MAPPING = seed_path / "cfbd-team-mapping.csv"
    insert_external_team_mappings(SR_TEAM_MAPPING, ds_code="SR")
    insert_external_team_mappings(ESPN_TEAM_MAPPING, ds_code="ESPN")
    insert_external_team_mappings(CFBDATA_TEAM_MAPPING, ds_code="CFBD")


def insert_external_team_mappings(f_path, ds_code: str):
    mappings = util.load_csv(f_path, headers=True)
    teams = {t.code: t for t in list_resources(models.Team)}
    sports_reference = meta.DataSource.query.filter_by(code=ds_code).one()
    for m in mappings:
        team = teams.get(m.get("hatchet-code"))
        value = m.get("school")
        ext_id = m.get("external-id", None)
        if not team:
            logger.error(f"unable to get team from {m.get('hatchet-code')}")
        mapper_model = meta.ExternalTeamIdentifier(
            team_id=team.id,
            source_id=sports_reference.id,
            value=value,
            external_id=ext_id
        )
        db.session.add(mapper_model)
    db.session.commit()
    logger.warning(f"created {ds_code} team mappings...")
    return 0


def insert_polls():
    POLLS = [
        models.Poll(code="AP", name="Associated Press", url="https://www.apnews.com/APTop25CollegeFootballPoll")
    ]
    db.session.add_all(POLLS)
    db.session.commit()
    logger.warning(f"created {len(POLLS)} polls in database...")
    return 0


def insert_rankings():
    do_rankings_for_season(2019)


def do_rankings_for_season(season: int):
    RANKINGS = seed_path / f"rankings-{season}.csv"
    rankings = util.load_csv(RANKINGS, headers=True, sort="Wk")
    weeks = {week.number: week for week in list_resources(models.Week, season=season)}

    for rank in rankings:
        team_name = util.strip_record(rank.get('School'))
        team = lookup_team_by_external_id(
            source="SportsReference", identifier=team_name
        )
        week = weeks.get(int(rank.get("Wk")))
        prior_week = weeks.get(week.number - 1, None)
        prior_ranking = None
        if prior_week:
            prior_ranking = models.Ranking.query\
                .filter_by(week_id=prior_week.id)\
                .filter_by(poll_id=1)\
                .filter_by(team_id=team.id)\
                .first()
        prior_rank = prior_ranking.rank if prior_ranking else None
        ranking = models.Ranking(
            week_id=week.id,
            poll_id=1,
            team_id=team.id,
            rank=rank.get("Rk"),
            prior_rank=prior_rank
        )
        db.session.add(ranking)
        db.session.commit()
    logger.warning(f"added rankings for {season} to database...")