from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.api.schemas import ConferenceSchema
from hatchet.db.models import Conference


conference_schema = ConferenceSchema()


def persist_conference(conference: dict) -> Conference:
    conference = conference_schema.load(conference, many=False)
    db.session.add(conference)
    db.session.commit()
    return conference


def list_conferences(conference_id: int = None) -> Union[Conference,
                                                         List[Conference]]:
    if not conference_id:
        return Conference.query.all()
    conference = Conference.query.filter_by(id=conference_id).first()
    if not conference:
        raise MissingResourceException(f'No Conference with id={conference_id}')
    return conference


def search_conferences(filters: List[dict]) -> List[Conference]:
    return []


def edit_conference(conference_id: int, conference: dict):
    old_conf = list_conferences(conference_id=conference_id)
    if not old_conf:
        raise MissingResourceException(f'No Conference with id={conference_id}')
    conference = conference_schema.load(conference, instance=old_conf)
    db.session.add(conference)
    db.session.commit()


def remove_conference_by_id(conference_id: int):
    conference = list_conferences(conference_id=conference_id)
    db.session.delete(conference)
    db.session.commit()
