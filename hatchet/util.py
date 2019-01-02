import csv
import json
from typing import List, Union


def load_json(file: str):
    with open(file, 'r') as fp:
        return json.load(fp.read())

def load_csv(file: str, headers=False) -> Union[List[list], List[dict]]:
    """ load a CSV into a list of rows or a list of json objects

    If the parameter `headers` is set to True, `load_csv` will return a
    list of json objects where each value is keyed on the column header.
    Otherwise, the default value of False will result in a list of tuples.

    Parameters
    ----------
    file
    headers

    Returns
    -------

    """
    if headers:
        data = load_csv(file, headers=False)
        hdrs = data[0]
        return [
            {
                xx: (yy if yy else None)
                for xx, yy in zip(hdrs, x)
            }
            for x in data[1:]
        ]
    with open(file, 'r', newline='', encoding='utf-8-sig') as fp:
        reader = csv.reader(fp, delimiter=',')
        return [x for x in reader]
