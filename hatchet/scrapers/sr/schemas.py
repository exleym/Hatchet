from marshmallow import Schema, fields


class SRSchoolSchema(Schema):
    school_name = fields.String(attribute="name")
    year_min = fields.Integer(attribute="start_year")
    year_max = fields.Integer(attribute="last_year")
    years = fields.Integer(attribute="seasons_played")
    g = fields.Integer(attribute="games_played")
    wins = fields.Integer(attribute="games_won")
    losses = fields.Integer(attribute="games_lost")
    ties = fields.Integer(attribute="games_tied")
    win_loss_pct = fields.Float(attribute="win_loss_pct")
    g_post = fields.Integer(attribute="g_post", allow_none=True)
    wins_post = fields.Integer(attribute="wins_post", allow_none=True)
    losses_post = fields.Integer(attribute="losses_post", allow_none=True)
    ties_post = fields.Integer(attribute="ties_post", allow_none=True)
    win_loss_pct_post = fields.Float(attribute="win_loss_pct_post", allow_none=True)
    srs = fields.Float(attribute="simple_rating_score")
    sos = fields.Float(attribute="strength_of_schedule")
    poll_final = fields.Integer(attribute="last_final_rank")
    conf_champ_count = fields.Integer(attribute="conf_champ_count")
    notes = fields.String(attribute="notes", required=False, allow_none=True)
