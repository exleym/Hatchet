from hatchet.db.models import LocationType
from hatchet.extensions import db


def populate_locations():
    db.session.add(LocationType(id=1, name='home'))
    db.session.add(LocationType(id=2, name='away'))
    db.session.add(LocationType(id=3, name='neutral site'))
