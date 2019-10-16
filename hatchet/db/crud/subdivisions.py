from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
# from hatchet.resources.schemas import ConferenceSchema
from hatchet.db.models import Conference


# conference_schema = ConferenceSchema()


def persist_conference(data: dict) -> Conference:
    # conference = conference_schema.load(conference, many=False)
    conference = Conference(**data)
    db.session.add(conference)
    db.session.commit()
    return conference


def list_conferences(conference_id: int = None,
                     code: str = None) -> Union[Conference, List[Conference]]:
    if conference_id:
        conf = Conference.query.filter_by(id=conference_id).first()
        if not conf:
            raise MissingResourceException(f'No Conference with id={conference_id}')
        return conf
    query = Conference.query
    if code:
        query = query.filter_by(code=code)
    return query.all()

#
# def search_conferences(filters: List[dict]) -> List[Conference]:
#     return []
#

def edit_conference(conference_id: int, data: dict):
    conference = list_conferences(conference_id=conference_id)
    if not conference:
        raise MissingResourceException(f'No Conference with id={conference_id}')
    _ = data.pop("id", None)
    for k, v in data.items():
        setattr(conference, k, v)
    db.session.add(conference)
    db.session.commit()
    return conference


def remove_conference_by_id(conference_id: int):
    conference = list_conferences(conference_id=conference_id)
    db.session.delete(conference)
    db.session.commit()
