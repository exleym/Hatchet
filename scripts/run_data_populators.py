import scripts.populate_conferences as populate_conferences
import scripts.populate_divisions as populate_divisions
import scripts.populate_teams as populate_teams
import scripts.populate_stadiums as populate_stadiums
import scripts.populate_games as populate_games

from hatchet import Environment


def main():
    populate_conferences.main()
    populate_divisions.main()
    populate_teams.main()
    populate_stadiums.main()
    populate_games.main()

if __name__ == '__main__':
    Environment.set(Environment.PROD)
    main()