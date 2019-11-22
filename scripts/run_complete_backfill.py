import logging
from typing import List
import scripts.populate_games as populate_games
import scripts.map_games_from_cfb as map_games_from_cfb
import scripts.populate_betting_data as populate_betting_data
import scripts.populate_ratings as populate_ratings


logging.basicConfig(level=logging.WARNING)
SEASONS = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
           2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


def main(seasons: List[int] = None):
    populate_games.run(seasons=seasons)
    map_games_from_cfb.run(seasons=seasons)
    populate_betting_data.run(seasons=seasons)
    # populate_ratings.run(seasons=seasons)


def run(seasons: List[int] = None):
    main(seasons=seasons)


if __name__ == "__main__":
    run(seasons=SEASONS)
