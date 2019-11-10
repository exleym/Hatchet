import dateutil.parser as dateparser
import logging
import pandas as pd
import pathlib
from hatchet.util import load_csv


logging.basicConfig(level=logging.INFO)
GAMEFILE = "hatchet/static/seeds/temp-games-2018.csv"
DEDUPED = "hatchet/static/seeds/games-2018.csv"
PATH = pathlib.Path(__file__).parent
logger = logging.getLogger(__name__)


def main(infile: str, outfile: str):
    f_in = PATH.parent / infile
    f_out = PATH.parent / outfile
    print(f_in.absolute())
    deduped = []
    original_games = load_csv(f_in, headers=True)
    processed_games = set()
    for game in original_games:
        date = dateparser.parse(game.get("Date"))
        game_info = frozenset([
            game.get("School"),
            game.get("Opponent"),
            date
        ])
        if game_info in processed_games:
            continue
        processed_games.add(game_info)
        deduped.append(game)
    df = pd.DataFrame.from_records(deduped)
    df.to_csv(f_out)


if __name__ == "__main__":
    main(GAMEFILE, DEDUPED)
