from hatchet.client.ext import CFBDataClient
from hatchet.client.hatchet_client import HatchetClient


cfb_client = CFBDataClient()
hatchet_client = HatchetClient()


def main():
    teams = cfb_client.get_teams(fbs_only=True)
    for team in teams:
        games = cfb_client.get_games(2019, team=team.name)
