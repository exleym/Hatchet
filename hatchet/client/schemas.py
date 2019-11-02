import logging
import marshmallow as ma
import hatchet.resources.schemas.schemas as schemas
import hatchet.client.models as cm


logger = logging.getLogger(__name__)


class HatchetClientMixin:

    model: type(cm.Resource)

    @ma.post_load
    def make_object(self, data, **kwargs):
        return self.model(**data)


class ClientSubdivisionSchema(schemas.SubdivisionSchema, HatchetClientMixin):
    model = cm.Subdivision


class ClientSurfaceSchema(schemas.SurfaceSchema, HatchetClientMixin):
    model = cm.Surface


class ClientStadiumSchema(schemas.StadiumSchema, HatchetClientMixin):
    model = cm.Stadium
    surface = ma.fields.Nested("ClientSurfaceSchema", missing=None, allow_none=True)


class ClientConferenceSchema(schemas.ConferenceSchema, HatchetClientMixin):
    model = cm.Conference


class ClientTeamSchema(schemas.TeamSchema, HatchetClientMixin):
    model = cm.Team
    stadium = ma.fields.Nested("ClientStadiumSchema", missing=None, allow_none=True)


class ClientGameSchema(schemas.GameSchema, HatchetClientMixin):
    model = cm.Game