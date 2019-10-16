import requests
from hatchet.util import load_csv


TEAM_PATH = '../hatchet/static/seeds/teams.csv'
UPLOAD_URL = 'http://localhost:5000/api/v1/teams/'
CONFERENCE_URL = 'http://localhost:5000/api/v1/conferences/'
DIVISION_URL = 'http://localhost:5000/api/v1/divisions/'

def main():
    raw_data = load_csv(TEAM_PATH, headers=True)
    conferences = load_conferences()
    divisions = load_divisions()
    for team in raw_data:
        conf = team.pop('conference')
        team['conferenceId'] = conferences.get(conf)
        div = team.pop('division')
        team['divisionId'] = divisions.get((team.get('conferenceId'), div))
        print(team)
        resp = requests.post(url=UPLOAD_URL, json=team)
        if resp.status_code != 201:
            print(resp.content)
        else:
            print(resp.json())

def load_conferences():
    resp = requests.get(url=CONFERENCE_URL)
    if resp.status_code == 200:
        return {c.get('code'): c.get('id') for c in resp.json()}
    return None


def load_divisions():
    resp = requests.get(url=DIVISION_URL)
    if resp.status_code == 200:
        return {
            (c.get('conferenceId'), c.get('name')):
                c.get('id') for c in resp.json()
        }
    return None



if __name__ == '__main__':
    main()
