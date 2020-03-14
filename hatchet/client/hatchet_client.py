import datetime as dt
import logging
import marshmallow as ma
from hatchet.client.base import ResourceClient
from hatchet.client.resource_clients import TeamClient
import hatchet.client.schemas as schemas
from hatchet.errors import MissingResourceException
from hatchet.util.validators import validate_xor


logger = logging.getLogger(__name__)


class HatchetClient(object):

    __EXTERNAL_CACHE = {}
    __TEAM_CACHE = {}
    __GAME_CACHE = {}
    domain = "http://localhost:8000/api/v1"

    def __init__(self):
        self.team_client = TeamClient(domain=self.domain,
                                      context="/teams",
                                      schema=schemas.ClientTeamSchema,
                                      model=TeamClient)
        self.conf_client = self.register_client(
            context="/conferences",
            schema=schemas.ClientConferenceSchema
        )
        self.game_client = self.register_client(
            context="/games",
            schema=schemas.ClientGameSchema
        )
        self.bookmaker_client = self.register_client(
            context="/bookmakers",
            schema=schemas.ClientBookmakerSchema
        )
        self.line_client = self.register_client(
            context="/lines",
            schema=schemas.ClientLineSchema
        )
        self.week_client = self.register_client(
            context="/weeks",
            schema=schemas.ClientWeekSchema
        )
        self.stadium_client = self.register_client(
            context="/stadiums",
            schema=schemas.ClientStadiumSchema
        )
        self.network_client = self.register_client(
            context="/networks",
            schema=schemas.ClientNetworkSchema
        )
        self.rating_client = self.register_client(
            context="/ratings",
            schema=schemas.ClientRatingSchema
        )

    def list_conferences(self, **kwargs):
        return self.conf_client.list_resources(**kwargs)

    def list_games(self, limit: int = None, offset: int = None):
        """get a list of Game objects from Hatchet

        keyword arguments work for paginating data, for filtering data, you
        should use the :meth:`find_game` method.
        """
        games = self.game_client.list_resources(limit=limit, offset=offset)
        self.__GAME_CACHE.update({g.id: g for g in games})
        return games

    def list_teams(self, limit: int = None, offset: int = None):
        """get a list of Team objects from Hatchet

        keyword arguments work for paginating data, for filtering data, you
        should use the :meth:`find_team` method.
        """
        teams = self.team_client.list_resources(limit=limit, offset=offset)
        self.__TEAM_CACHE.update({t.id: t for t in teams})
        return teams

    def list_lines(self):
        return self.line_client.list_resources()

    def list_networks(self):
        """get a list of Networks from Hatchet API

        Networks represent the various television stations / networks. In a
        future version, we will create a hierarchy of these up to parent
        networks to allow for more sensible aggregation, but for now, we treat
        each channel as an independent network.
        """
        return self.network_client.list_resources()

    def list_ratings(self):
        """get a list of Rating objects from Hatchet.

        Rating objects are 1:1 associated with games and contain information
        about the airing network and the number of viewers for the game. In
        this version, we do not differentiate between streaming and TV viewers.
        """
        return self.rating_client.list_resources()

    def get_team(self, id: int = None, code: str = None):
        """get a single Team by its id or code identifier"""
        if id:
            team = self.__TEAM_CACHE.get(id)
            if team: return team
            team = self.team_client.get_resource_by_id(id=id)
            self.__TEAM_CACHE[team.id] = team
            return team
        return self.team_client.get_resource_by_code(code=code)


    def find_team(self, query: str):
        """find a team with a partial match against short-name or name

        search query will attempt to match against short-name, and if it fails
        to find a match, search again against name. it is a known limitation
        that this will not be the union of matches against short-name and name
        but rather the matches against short-name with a fail-over to the
        matches against name.
        """
        v = f"%{query}%"
        team = self.team_client.search(field="shortName", op="like", value=v)
        if not team:
            team = self.team_client.search(field="name", op="like", value=v)
        return team

    def clear_ratings(self):
        ratings = self.list_ratings()
        for rating in ratings:
            self.rating_client.delete_resource(rating.id)

    def create_network(self, code: str, name: str, website: str = None):
        return self.network_client.create_resource(
            code=code,
            name=name,
            website=website
        )

    def create_line(self, game_id: int, team_id: int, bookmaker_id: int,
                    spread: float, over_under: float = None, vigorish: int = None):
        return self.line_client.create_resource(
            game_id=game_id,
            team_id=team_id,
            bookmaker_id=bookmaker_id,
            spread=spread,
            over_under=over_under,
            vigorish=vigorish
        )


    def create_team(self, code: str, name: str, short_name: str, mascot: str,
                    conference_id: int, division_id: int, stadium_id: int):
        """create a new Hatchet team and return the new Team object"""
        return self.team_client.create_resource(
            code=code, name=name, short_name=short_name, mascot=mascot,
            conference_id=conference_id, division_id=division_id,
            stadium_id=stadium_id
        )


    def add_external_mapping(self, team_id: int, external_name: str =  None,
                             external_id: int = None):
        """create an external data-source mapping for a team"""
        pass

    def get_team_by_external_id(self, name: str, source: str):
        """get a team by an external mapping identifier

        external data sources key data on integer ids, string team names, or
        a combination of both. behind the scenes we are maintaining mappings
        from our team objects to each of these external identifiers. this
        method does a reverse-lookup from external id to team.
        """
        team = self.__EXTERNAL_CACHE.get((name, source))
        if not team:
            team = self.team_client.get_team_by_external_id(
                name=name, source=source
            )
            self.__EXTERNAL_CACHE[(name, source)] = team
        return team

    def get_team_games(self, team_id: int, season: int = None,
                       date: dt.date = None):
        return self.team_client.get_team_games(team_id=team_id, season=season,
                                               date=date)

    def find_game(self, team_id: int, date: dt.date):
        games = self.get_team_games(team_id=team_id, date=date)
        if games:
            return games[0]
        return None

    def get_game(self, id: int = None, espn_id: int = None):
        validate_xor(id=id, espn_id=espn_id)
        if id:
            return self.game_client.get_resource_by_id(id=id)
        games = self.game_client.search("espnId", "=", espn_id)
        if not games:
            raise MissingResourceException(f"no game with ESPN id = {espn_id}")
        return games[0]

    def get_bookmakers(self, **kwargs):
        return self.bookmaker_client.list_resources(**kwargs)

    def update_game(self, game):
        return self.game_client.update_resource(game)

    def delete_line(self, id: int):
        return self.line_client.delete_resource(id=id)

    def clear_lines(self):
        logger.warning(f"clearing lines from Hatchet database...")
        lines = self.list_lines()
        for line in lines:
            self.delete_line(id=line.id)
        logger.warning(f"{len(lines)} lines removed.")

    def list_weeks(self, season: int):
        return self.week_client.list_resources(season=season)

    def register_client(self, context: str, schema: type(ma.Schema),
                        model: type(ResourceClient) = None):
        model = model or ResourceClient
        return model(
            domain=self.domain,
            context=context,
            schema=schema,
            model=schema.model
        )

    def get_stadium_by_external_id(self, name: str, source: str):
        raise NotImplementedError

    def list_networks(self):
        return self.network_client.list_resources()

    def create_rating(self, game_id: int, network_id: int, rating: float = None,
                      viewers: float = None):
        return self.rating_client.create_resource(
            game_id=game_id,
            network_id=network_id,
            rating=rating,
            viewers=viewers
        )