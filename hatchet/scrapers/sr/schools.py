from bs4.element import Tag
from typing import List

from hatchet.scrapers.base import Scraper
from hatchet.scrapers.sr.schemas import SRSchoolSchema
from hatchet.scrapers.sr.models import SRSchool


class SchoolScraper(Scraper):
    _url = "http://www.sports-reference.com/cfb/schools/"
    school_schema = SRSchoolSchema()

    def load(self) -> List[SRSchool]:
        raw_teams = self.get_teams()
        teams = self.school_schema.load(raw_teams, many=True)
        return [SRSchool(**team) for team in teams if team]

    def get_teams(self):
        """fetch html from site and process it into SRTeam objects

        SRTeam objects are specific to the data provided by Sports-Reference
        and are not perfectly mapped to our data model, so there will be some
        fields contained in this response that we discard, and some that must
        be filled in elsewhere.
        """
        soup = self.get_soup()
        team_table = soup.find(name="tbody")
        teams = team_table.findAll("tr")
        return [self.process_team(team) for team in teams]

    def process_team(self, team: Tag):
        stats = team.findAll("td")
        return {
            el.attrs.get("data-stat"): self.extract_from_td(el)
            for el in stats
            if el.attrs.get("data-stat") is not None
        }

