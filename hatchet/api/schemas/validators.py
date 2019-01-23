# Define schema validators for various field types
import datetime


MODERNITY = datetime.datetime(1880, 1, 1, 0, 0, 0)


def modern_date_validator(value):
    now = datetime.date.today()
    return value > MODERNITY.date() and value <= now

def modern_datetime_validator(value):
    year = datetime.date.today().year + 2
    next_year = datetime.datetime(year, 12, 31, 0, 0, 0)
    return value > MODERNITY and value <= next_year


def modern_year_validator(value):
    now = datetime.date.today().year
    return value > MODERNITY.year and value <= now

def score_validator(value):
    if not value:
        return True
    return value >= 0 and value < 100
