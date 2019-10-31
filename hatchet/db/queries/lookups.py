import logging
import hatchet.db.meta_models as meta


logger = logging.getLogger(__name__)


def lookup_team_by_external_id(source: str, identifier: str):
    src = meta.DataSource.query.filter_by(name=source).one()
    ext_id = meta.ExternalTeamIdentifier.query \
        .filter_by(source_id=src.id) \
        .filter_by(value=identifier) \
        .one()
    return ext_id.team