import requests
from hatchet.util import load_csv


CONFERENCE_PATH = '../hatchet/static/seeds/conferences.csv'
UPLOAD_URL = 'http://localhost:5000/api/v1/conferences'

def main():
    raw_data = load_csv(CONFERENCE_PATH, headers=True)
    for conference in raw_data:
        resp = requests.post(url=UPLOAD_URL, json=conference)
        print(resp)
        if resp.status_code != 201:
            print(conference)
            print(resp.content)


if __name__ == '__main__':
    main()
