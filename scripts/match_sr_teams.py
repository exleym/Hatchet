from fuzzywuzzy import process
import requests
from hatchet.scrapers.sr.schools import SchoolScraper

scraper = SchoolScraper()


def main():
    schools = scraper.load()
    sr_school_names = [s.name for s in schools if s.last_year > 2000]
    teams = load_teams()
    for t in teams:
        # print(f"looking for a match for {t}")
        best_match(t, sr_school_names)


def load_teams():
    resp = requests.get("http://localhost:5000/api/v1/teams")
    teams = resp.json()
    return [t.get("name") for t in teams]


def best_match(string, choices):
    highest = process.extractOne(string, choices)
    match = highest[0]
    conf = highest[1]
    print(f"i think the best match for {string} is {match} ({conf}).")


if __name__ == "__main__":
    main()
