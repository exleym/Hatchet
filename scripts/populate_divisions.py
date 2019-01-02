import requests
from hatchet.util import load_csv


DIVISION_PATH = '../hatchet/static/seeds/divisions.csv'
UPLOAD_URL = 'http://localhost:5000/api/v1/divisions'
CONFERENCE_URL = 'http://localhost:5000/api/v1/conferences'

def main():
    raw_data = load_csv(DIVISION_PATH, headers=True)
    conferences = load_conferences()
    for division in raw_data:
        conf = division.pop('conference')
        division['conferenceId'] = conferences.get(conf)
        resp = requests.post(url=UPLOAD_URL, json=division)
        print(resp)
        if resp.status_code != 201:
            print(division)
            print(resp.content)


def load_conferences():
    resp = requests.get(url=CONFERENCE_URL)
    if resp.status_code == 200:
        return {c.get('code'): c.get('id') for c in resp.json()}
    return None


if __name__ == '__main__':
    main()
