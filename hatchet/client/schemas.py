import logging
import marshmallow as ma
import hatchet.resources.schemas.schemas as schemas
import hatchet.client.models as cm


logger = logging.getLogger(__name__)


class HatchetClientMixin:

    model: type(cm.Resource)

    @ma.post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        try:
            return self.model(**data)
        except TypeError as e:
            logger.error(f"error loading {self.model} from {data}...")
            raise e


class ClientBookmakerSchema(schemas.BookmakerSchema, HatchetClientMixin):
    model = cm.Bookmaker


class ClientSubdivisionSchema(schemas.SubdivisionSchema, HatchetClientMixin):
    model = cm.Subdivision


class ClientSurfaceSchema(schemas.SurfaceSchema, HatchetClientMixin):
    model = cm.Surface


class ClientStadiumSchema(schemas.StadiumSchema, HatchetClientMixin):
    model = cm.Stadium
    surface = ma.fields.Nested("ClientSurfaceSchema", missing=None, allow_none=True)

    @ma.post_load
    def make_object(self, data, **kwargs):
        if not data.get("code"):
            return None
        return self.model(**data)


class ClientConferenceSchema(schemas.ConferenceSchema, HatchetClientMixin):
    model = cm.Conference
    subdivision = ma.fields.Nested("ClientSubdivisionSchema", missing=None, allow_none=True)


class ClientDivisionSchema(schemas.DivisionSchema,HatchetClientMixin):
    model = cm.Division
    conference = ma.fields.Nested("ClientConferenceSchema", missing=None, allow_none=None)


class ClientTeamSchema(schemas.TeamSchema, HatchetClientMixin):
    model = cm.Team
    stadium = ma.fields.Nested("ClientStadiumSchema", missing=None, allow_none=True)
    division = ma.fields.Nested("ClientDivisionSchema", missing=None, allow_none=True)


class ClientGameParticipantSchema(schemas.GameParticipantSchema, HatchetClientMixin):
    model = cm.Participant
    team = ma.fields.Nested("ClientTeamSchema")


class ClientNetworkSchema(schemas.NetworkSchema, HatchetClientMixin):
    model = cm.Network


class ClientRatingSchema(schemas.RatingSchema, HatchetClientMixin):
    model = cm.Rating


class ClientGameSchema(schemas.GameSchema, HatchetClientMixin):
    model = cm.Game
    participants = ma.fields.List(ma.fields.Nested("ClientGameParticipantSchema"), load_only=True)
    winner = ma.fields.Nested("ClientGameParticipantSchema",load_only=True)
    # rating = ma.fields.List(ma.fields.Nested("ClientRatingSchema", required=False,
    #                           allow_none=True, many=False))


class ClientLineSchema(schemas.LineSchema, HatchetClientMixin):
    model = cm.Line

    game = ma.fields.Nested("ClientGameSchema")
    team = ma.fields.Nested("ClientTeamSchema")
    bookmaker = ma.fields.Nested("ClientBookmakerSchema", required=False,
                                 allow_none=True)


class ClientWeekSchema(schemas.WeekSchema, HatchetClientMixin):
    model = cm.Week
