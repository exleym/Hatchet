import marshmallow as ma
import hatchet.client.ext.cfb.models as models


class FBSClientSchema(ma.Schema):

    model = None

    def on_bind_field(self, field_name, field_obj):
        """automatically allow nulls for all fields"""
        super().on_bind_field(field_name, field_obj)
        field_obj.allow_none = True
        field_obj.missing = None

    @ma.post_load
    def make_object(self, data, **kwargs):
        return self.model(**data)


class GameSchema(FBSClientSchema):

    model = models.Game

    id = ma.fields.Integer()
    season = ma.fields.Integer()
    week = ma.fields.Integer()
    season_type = ma.fields.String()
    start_date = ma.fields.DateTime()
    neutral_site = ma.fields.Boolean()
    conference_game = ma.fields.Boolean()
    attendance = ma.fields.Float()
    venue_id = ma.fields.Integer()
    venue = ma.fields.String()
    home_team = ma.fields.String()
    home_conference = ma.fields.String()
    home_points = ma.fields.Integer()
    home_line_scores = ma.fields.List(ma.fields.Integer())
    away_team = ma.fields.String()
    away_conference = ma.fields.String()
    away_points = ma.fields.Integer()
    away_line_scores = ma.fields.List(ma.fields.Integer())


class TeamSchema(FBSClientSchema):

    model = models.Team

    id = ma.fields.Integer()
    school = ma.fields.String()
    mascot = ma.fields.String()
    abbreviation = ma.fields.String()
    alt_name1 = ma.fields.String(attribute="alt_name_1")
    alt_name2 = ma.fields.String(attribute="alt_name_2")
    alt_name3 = ma.fields.String(attribute="alt_name_3")
    conference = ma.fields.String()
    division = ma.fields.String()
    color = ma.fields.String()
    alt_color = ma.fields.String()
    logos = ma.fields.List(ma.fields.String())
