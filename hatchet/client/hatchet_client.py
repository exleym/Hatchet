import datetime as dt
import marshmallow as ma
from hatchet.client.base import ResourceClient
from hatchet.client.resource_clients import TeamClient
import hatchet.client.schemas as schemas


class HatchetClient(object):

    domain = "http://localhost:5000/api/v1"

    def __init__(self):
        self.team_client = TeamClient(domain=self.domain,
                                      context="/teams",
                                      schema=schemas.ClientTeamSchema,
                                      model=TeamClient)
        self.conf_client = self.register_client(
            context="/conferences",
            schema=schemas.ClientConferenceSchema
        )

    def list_teams(self, limit: int = None, offset: int = None):
        """get a list of Team objects from Hatchet

        keyword arguments work for paginating data, for filtering data, you
        should use the :meth:`find_team` method.
        """
        return self.team_client.list_resources(limit=limit, offset=offset)

    def get_team(self, id: int = None, code: str = None):
        """get a single Team by its id or code identifier"""
        if id:
            return self.team_client.get_resource_by_id(id=id)
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

    def get_team_by_external_id(self, name: str, source: str):
        """get a team by an external mapping identifier

        external data sources key data on integer ids, string team names, or
        a combination of both. behind the scenes we are maintaining mappings
        from our team objects to each of these external identifiers. this
        method does a reverse-lookup from external id to team.
        """
        return self.team_client.get_team_by_external_id(
            name=name, source=source
        )

    def add_external_mapping(self, team_id: int, external_name: str =  None,
                             external_id: int = None):
        """create an external data-source mapping for a team



        Parameters
        ----------
        team_id
        external_name
        external_id

        Returns
        -------

        """


    def create_team(self, code: str, name: str, short_name: str, mascot: str,
                    conference_id: int, division_id: int, stadium_id: int):
        """create a new Hatchet team and return the new Team object"""
        return self.team_client.create_resource(
            code=code, name=name, short_name=short_name, mascot=mascot,
            conference_id=conference_id, division_id=division_id,
            stadium_id=stadium_id
        )

    def get_team_games(self, team_id: int, season: int = None):
        return self.team_client.get_team_games(team_id=team_id, season=season)


    def list_conferences(self, **kwargs):
        return self.conf_client.list_resources(**kwargs)

    def find_game(self, team_id: int, date: dt.date):
        games = self.get_team_games(team_id=team_id, season=date.year)
        match = [g for g in games if g.game_time.date() == date]
        if match:
            return match[0]
        return None

    def register_client(self, context: str, schema: type(ma.Schema),
                        model: type(ResourceClient) = None):
        model = model or ResourceClient
        return model(
            domain=self.domain,
            context=context,
            schema=schema,
            model=schema.model
        )