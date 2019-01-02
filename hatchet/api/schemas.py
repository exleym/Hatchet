from marshmallow import post_load
from hatchet.extensions import ma
from hatchet.db.models import Conference, Division, Stadium, Team


class ConferenceSchema(ma.ModelSchema):
    class Meta:
        model = Conference
    id = ma.Int(dump_only=True)
    code = ma.Str()
    name = ma.Str()
    shortName = ma.Str(attribute='short_name', allow_none=True)
    inceptionYear = ma.Int(attribute="inception_year",
                               validate=lambda x: 1850 < x < 2018,
                               allow_none=True)
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_conference_by_id', conference_id='<id>'),
        'collection': ma.URLFor('api.get_conferences'),
        'members': ma.URLFor('api.get_conference_members', conference_id='<id>'),
        'divisions': ma.URLFor('api.get_conference_divisions', conference_id='<id>')
    })


class DivisionSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    conferenceId = ma.Int(attribute='conference_id')
    name = ma.Str(allow_none=True)
    fullName = ma.Str(attribute='full_name', dump_only=True)

    links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_division_by_id', division_id='<id>'),
        'collection': ma.URLFor('api.get_divisions'),
        'members': ma.URLFor('api.get_division_members',division_id='<id>'),
        #'conference': ma.URLFor('api.get_conference_by_id', conference_id='<conference_id>')
    })

    @post_load
    def make_object(self, data):
        return Division(**data)


class StadiumSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    name = ma.Str()
    nickname = ma.Str(allow_none=True)
    built = ma.Int()
    capacity = ma.Int()

    links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_stadium_by_id', stadium_id='<id>'),
        'collection': ma.URLFor('api.get_stadiums'),
    })

    @post_load
    def make_object(self, data):
        return Stadium(**data)


class TeamSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    name = ma.Str()
    shortName = ma.Str(attribute='short_name', allow_none=True)
    mascot = ma.Str()
    conferenceId = ma.Int(attribute='conference_id')
    divisionId = ma.Int(attribute='division_id')
    stadiumId = ma.Int(attribute='stadium_id', allow_none=True)

    links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_team_by_id', team_id='<id>'),
        'collection': ma.URLFor('api.get_teams'),
        'conference': ma.URLFor('api.get_conference_by_id', conference_id='<conference_id>'),
        'division': ma.URLFor('api.get_division_by_id', division_id='<division_id>')})

    #stadium = fields.Nested(StadiumSchema)

    @post_load
    def make_object(self, data):
        return Team(**data)