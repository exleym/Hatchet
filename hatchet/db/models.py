from flask import url_for
from hatchet.extensions import db


team_stadium_association = db.Table(
    'team_stadium_association',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('stadium_id', db.Integer, db.ForeignKey('stadium.id'))
)


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    short_name = db.Column(db.String(32), unique=True, nullable=True)
    inception_year = db.Column(db.Integer)

    @property
    def links(self):
        return dict()

    def __repr__(self):
        return f"<Conference(id={self.id}, code='{self.code}'," \
               f" name='{self.name})>"


class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    name = db.Column(db.String, nullable=True)

    conference = db.relationship('Conference', backref='divisions')

    @property
    def standings(self):
        teams = self.members
        teams.sort(key=lambda x: x.wins, reverse=True)
        return teams

    @property
    def full_name(self):
        conference = self.conference.short_name or self.conference.name
        if self.name:
            return f"{conference} - {self.name}"
        return self.conference.name

    def __repr__(self):
        return f"<Division(id={self.id}, conference_id={self.conference_id}," \
               f" name='{self.name})>"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_time = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'))
    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)

    home_team = db.relationship('Team', backref='home_games',
                                foreign_keys=[home_team_id])
    away_team = db.relationship('Team', backref='away_games',
                                foreign_keys=[away_team_id])

    @property
    def date(self):
        return self.game_time.date()

    @property
    def kickoff_time(self):
        return self.game_time.strftime('%H:%M:%S')

    @property
    def winner(self):
        if self.home_team_score > self.away_team_score:
            return self.home_team
        return self.away_team

    @property
    def loser(self):
        if self.home_team_score < self.away_team_score:
            return self.home_team
        return self.away_team

    def __repr__(self):
        return f"<Game({self.away_team.short_name} @ {self.home_team.short_name}" \
               f")>"


class Stadium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    nickname = db.Column(db.String(64))
    built = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    surface = db.Column(db.String(128))

    def __repr__(self):
        return f"<Stadium(id={self.id}, name='{self.name}', " \
               f"nickname='{self.nickname}')>"

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    short_name = db.Column(db.String(64), nullable=True)
    mascot = db.Column(db.String(128), nullable=False)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'))

    conference = db.relationship('Conference', backref='members')
    division = db.relationship('Division', backref='members')
    stadium = db.relationship('Stadium', uselist=False, backref='team')

    @property
    def wins(self):
        return len([g for g in self.games if g.winner_id == self.id])

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', " \
               f"mascot='{self.mascot}')>"
