from hatchet.extensions import db


class DataSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(128), unique=True)
    url = db.Column(db.String(256))


class ExternalTeamIdentifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    source_id = db.Column(db.Integer, db.ForeignKey("data_source.id"))
    value = db.Column(db.String(128))
    external_id = db.Column(db.Integer, nullable=True)

    team = db.relationship("Team", backref="external_identifiers")


class ExternalGameIdentifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))