import logging
import requests
from hatchet.client.hatchet_client import ResourceClient
from hatchet.resources.schemas.schemas import TeamSchema


logger = logging.getLogger(__name__)
schema = TeamSchema()


class TeamClient(ResourceClient):

    def get_team_by_external_id(self, name: str, source: str):
        pkg = {"dataSource": source, "teamName": name}
        try:
            data = self.post_data(
                f"{self.base_url}/external/search", body=pkg
            )
            team = self.unwrap(data)
            return team
        except requests.exceptions.HTTPError:
            logger.error(f"no Team with id={name} for source={source}...")
        team = None
        return team
