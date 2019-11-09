import logging
import hatchet.db.meta_models as meta
import hatchet.errors as errors


logger = logging.getLogger(__name__)


def lookup_team_by_external_id(source: str, identifier: str):
    src = meta.DataSource.query.filter_by(name=source).first()
    if not src:
        message = f"{source} is not a valid data source."
        raise errors.InvalidArgumentError(message)
    ext_id = meta.ExternalTeamIdentifier.query \
        .filter_by(source_id=src.id) \
        .filter_by(value=identifier) \
        .first()
    if not ext_id:
        raise errors.MissingResourceException(
            message=f"no team is mapped with external id = {identifier} "
                    f"and source = {source}."
        )
    return ext_id.team
