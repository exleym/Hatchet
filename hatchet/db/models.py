from hatchet.extensions import db


team_stadium_association = db.Table(
    'team_stadium_association',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('stadium_id', db.Integer, db.ForeignKey('stadium.id'))
)


class Subdivision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8))
    name = db.Column(db.String(32))
    division = db.Column(db.Integer)

    @property
    def teams(self):
        _teams = []
        for c in self.conferences:
            _teams += c.members
        return _teams

    def __repr__(self):
        return f"<Subdivision(id={self.id}, code='{self.code}')>"


class Surface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16))
    name = db.Column(db.String(128))
    category = db.Column(db.String(8))

    def __repr__(self):
        return f"<Surface(id={self.id}, code='{self.code}', " \
               f"name='{self.name}')>"



class GameParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    location_type_id = db.Column(db.Integer, db.ForeignKey('location_type.id'))
    score = db.Column(db.Integer)

    def __repr__(self):
        return f"<GameParticipant(team_id={self.team_id}, game_id={self.game_id}," \
               f"score={self.score})>"


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subdivision_id = db.Column(db.Integer, db.ForeignKey("subdivision.id"))
    code = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    short_name = db.Column(db.String(32), unique=True, nullable=True)
    inception_year = db.Column(db.Integer)

    subdivision = db.relationship("Subdivision", backref="conferences")

    @property
    def links(self):
        return dict()

    def __repr__(self):
        return f"<Conference(id={self.id}, code='{self.code}'," \
               f" name='{self.name}, short_name='{self.short_name}')>"


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
    espn_id = db.Column(db.Integer, nullable=True)

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
        max_scorer = None
        for p in self.participants:
            if p.score and p.score > max_score:
                max_score = p.score
                max_scorer = p
        return max_scorer

    @property
    def loser(self):
        min_score = 9999
        min_scorer = None
        for p in self.participants:
            if p.score and p.score < min_score:
                min_score = p.score
                min_scorer = p
        return min_scorer
    def __repr__(self):
        return f"<Game(id={self.id})>"


class Stadium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16))
    name = db.Column(db.String(128))
    state = db.Column(db.String(2))
    city = db.Column(db.String(64))
    latitude = db.Column(db.String(16))
    longitude = db.Column(db.String(16))
    built = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    surface_id = db.Column(
        db.Integer,
        db.ForeignKey("surface.id")
    )

    surface = db.relationship("Surface", backref="stadiums")

    def __repr__(self):
        return f"<Stadium(id={self.id}, name='{self.name}')>"

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True)
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

    @property
    def games(self):
        return [g.game for g in self.played_in]

    @property
    def home_games(self):
        return [g.game for g in self.played_in if g.location_type_id==1]

    @property
    def wins(self):
        return len(
            [
                g for g in self.games
                if g.winner and g.winner.team_id == self.id
            ])

    @property
    def losses(self):
        return len(
            [
                g for g in self.games
                if g.winner and g.winner.team_id != self.id
            ])

    @property
    def conference_wins(self):
        return len(
            [
                g for g in self.games
                if g.winner
                   and g.winner.team_id == self.id
                   and g.loser.team.conference_id == self.conference_id
            ])

    @property
    def conference_losses(self):
        return len([
            g for g in self.games
            if g.winner
               and g.winner.team_id != self.id
               and g.winner.team.conference_id == self.conference_id
        ])

    def record(self, season: int):
        return {
            "season": season,
            "wins": self.wins,
            "losses": self.losses,
            "confWins": self.conference_wins,
            "confLosses": self.conference_losses
        }


    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', " \
               f"mascot='{self.mascot}', code='{self.code}')>"


class LocationType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return f"<LocationType(id={self.id}, name='{self.name}')>"


class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quarter = db.Column(db.Integer)
    play_number = db.Column(db.Integer)
    game_clock = db.Column(db.Time)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    down = db.Column(db.Integer)
    to_go = db.Column(db.Float)
    play_occurred = db.Column(db.Boolean)
    penalty_occurred = db.Column(db.Boolean)

    game = db.relationship("Game", backref="plays")


class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dob = db.Column(db.Date, nullable=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dob = db.Column(db.Date, nullable=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Bookmaker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(128), unique=True)
    website = db.Column(db.String(256))


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    bookmaker_id = db.Column(db.Integer, db.ForeignKey("bookmaker.id"))
    spread = db.Column(db.Float)
    over_under = db.Column(db.Float)
    vigorish = db.Column(db.Integer)


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    season = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(16))
    name = db.Column(db.String(128))
    url = db.Column(db.String(256))


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"))
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    rank = db.Column(db.Integer)
    prior_rank = db.Column(db.Integer)

    poll = db.relationship("Poll")
    team = db.relationship("Team")