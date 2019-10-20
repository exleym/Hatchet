import csv
from flask_restplus import Namespace
from flask_restplus.reqparse import RequestParser
import json
import re
from typing import List, Union


def default_list_parser(namespace: Namespace) -> RequestParser:
    parser = namespace.parser()
    parser.add_argument(
        "limit",
        type=int,
        required=False,
        help="number of items to include in response",
        location="args"
    )
    parser.add_argument(
        "offset",
        type=int,
        required=False,
        help="number of items to offset from the start of response",
        location="args"
    )
    return parser



def load_json(file: str):
    with open(file, 'r') as fp:
        return json.load(fp.read())


def load_csv(file: str, headers=False) -> List[dict]:
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


def validate_xor(**kwargs):
    try:
        assert sum(x is not None for x in kwargs.values()) == 1
    except AssertionError:
        raise ValueError(
            f"one and only one of {kwargs.values()} must be non null"
        )


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def _camel_to_snake(camel: str) -> str:
    s1 = first_cap_re.sub(r'\1_\2', camel)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def camel_to_snake(data: Union[list, dict]) -> Union[list, dict]:
    if isinstance(data, list):
        return [camel_to_snake(x) for x in data]
    new = {}
    for k, v in data.items():
        if isinstance(v, (dict, list)):
            v = camel_to_snake(v)
        new.update({_camel_to_snake(k): v})
    return new
