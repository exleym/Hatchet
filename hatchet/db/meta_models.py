from hatchet.extensions import db


class DataSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    url = db.Column(db.String(256))
