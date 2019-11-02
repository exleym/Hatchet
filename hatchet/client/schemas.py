import marshmallow as ma
import hatchet.resources.schemas.schemas as schemas
import hatchet.client.models as client_models


class HatchetClientMixin:

    model: type(client_models.Resource)

    @ma.post_load
    def make_object(self, data, **kwargs):
        return self.model(**data)


class ClientSubdivisionSchema(schemas.SubdivisionSchema, HatchetClientMixin):
    model = client_models.Subdivision


class ClientConferenceSchema(schemas.ConferenceSchema, HatchetClientMixin):
    model = client_models.Conference


class ClientTeamSchema(schemas.TeamSchema, HatchetClientMixin):
    model = client_models.Team
