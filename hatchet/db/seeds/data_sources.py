from collections import namedtuple

DataSource = namedtuple("DataSource", "code name url")

DATA_SOURCES = [
    DataSource("BOV", "Bovada", "http://www.bovada.lv"),
    DataSource("SR", "SportsReference", "http://www.sports-reference.com/cfb"),
    DataSource("ESPN", "ESPN", "http://www.espn.com"),
]
