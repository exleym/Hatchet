from flask import url_for
from hatchet.extensions import db


team_stadium_association = db.Table(
    'team_stadium_association',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('stadium_id', db.Integer, db.ForeignKey('stadium.id'))
)


class GameParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    location_type_id = db.Column(db.Integer, db.ForeignKey('location_type.id'))
    score = db.Column(db.Integer)


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
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'))

    participants = db.relationship('GameParticipant', backref='game')

    @property
    def date(self):
        return self.game_time.date()

    @property
    def kickoff_time(self):
        return self.game_time.strftime('%H:%M:%S')

    @property
    def winner(self):
        max_score = 0
        for p in self.participants:
            if p.score and p.score > max_score:
                max_score = p.score
        for p in self.participants:
            if p.score == max_score:
                return p
        return None

    @property
    def loser(self):
        if self.home_team_score < self.away_team_score:
            return self.home_team
        return self.away_team

    def __repr__(self):
        return f"<Game(id={self.id})>"


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
    played_in = db.relationship('GameParticipant', backref='team')

    #todo: home_games and away_games relationships based off the location_type_id in the assoc table
    # these relationships are dependent on that extra join where game_participant.location_type_id == 1
    # and shit like that. This feels really janky, but it might work one it's implemented. Really all we need
    # here is something that lets you get home and away games from a team and find out if there's a home team for
    # each game. Do neutral site games have a fake home team each year? We want to represent neutral games as
    # x vs y rather than x @ y or y @ x. For a team's scheduel how do we differentiate?
    # Home: [X] @ [Y}
    # Away: [Y] @ [X]
    # Neutral: [X] vs [Y] where [X] is the team you're looking at, and [Y] is the other team

    @property
    def home_games(self):
        return [g.game for g in self.played_in if g.location_type_id==1]

    @property
    def wins(self):
        return len([g for g in self.games if g.winner_id == self.id])

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', " \
               f"mascot='{self.mascot}')>"


class LocationType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return f"<LocationType(id={self.id}, name='{self.name}')>"


class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    play_number = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    down = db.Column(db.Integer)
    to_go = db.Column(db.Float)
    snapped = db.Column(db.Boolean)

